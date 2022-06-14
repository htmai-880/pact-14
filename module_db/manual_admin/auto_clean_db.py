import re
from tqdm import tqdm
from server.ai.app.ai.db import DB
# import pickle
# import atexit

# # function is executed before script terminates
# def exit_handler():
#     with open("clean_db_train_data.pickle", "wb") as output_file:
#         pickle.dump(clean_db_train_data, output_file)
#
#
# atexit.register(exit_handler)
#
# try:
#     with open("clean_db_train_data.pickle", "rb") as input_file:
#         clean_db_train_data = pickle.load(input_file)
# except FileNotFoundError:
#     clean_db_train_data = []

# connect to db
db = DB()


# function to merge same ingredients
def merge_ingredients():
    db.run("""
    MATCH (i:Ingredient)
    MATCH (ii:Ingredient)
    WHERE toLower(i.name) = toLower(ii.name) AND i <> ii
    CALL apoc.refactor.mergeNodes([i,ii], {properties: {
        name:'discard'}})
    YIELD node
    RETURN node
    """)
    db.run("""
        MATCH (i:Ingredient)
        WHERE size((i)<-[:HAS_INGREDIENT]-(:Recipe))=0
        DETACH DELETE (i)
        """)


# convert instructions text to list
print("Converting instructions text to list...")
db.run("""
    MATCH (r:Recipe)
    WHERE apoc.meta.type(r.instructions) = "STRING"
    SET r.instructions = split(r.instructions,"\n")
    """)
db.run("""
    MATCH (r:Recipe)
    WHERE apoc.meta.type(r.instructions) = "STRING"
    SET r.instructions = split(r.instructions,". ")
    """)

# clean "to taste" ingredients
print("Clean 'to taste' ingredients...")
recipes_to_clean = db.run(r"""MATCH (i:Ingredient)
WHERE i.name CONTAINS " to taste"
RETURN i.name AS name, id(i) AS id""")

for recipe in tqdm(recipes_to_clean):
    name = recipe['name'].replace(" to taste", '')
    r_id = recipe['id']
    db.run(f"""
    MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
    WHERE id(i)={r_id}
    SET i.name = "{name}",
    h.option = {True}""")

# *** "(dd unit) name" format ***
print("Cleaning '(dd unit) name' format...")
recipes_to_clean = db.run(r"""MATCH (i:Ingredient)
WHERE i.name =~ ".*?\([0-9\./]*[ -].*?\) .*"
RETURN i.name AS name, id(i) AS id""")

merge_ingredients()

# (10.75 ounce) cans condensed cream of chicken soup
for recipe in tqdm(recipes_to_clean):
    matches = re.search(r"(.*?)\(([0-9./]*)[ -](.*?)\) (.*)", recipe['name'], re.IGNORECASE)
    if matches:
        beginning = matches.group(1)
        quantity = matches.group(2)
        unit = matches.group(3)
        end = matches.group(4)
        name = beginning + end

        r_id = recipe['id']
        r_name = recipe['name']

        # input(f"{r_name} : {quantity} {unit} {name}")

        # parse qn as float
        if '/' in quantity:
            matches = re.search(r"([0-9]+)/([0-9]+)", quantity, re.IGNORECASE)
            if matches:
                qn, qd = int(matches.group(1)), int(matches.group(2))
            else:
                qn, qd = 0, 0
        else:
            quantity = float(quantity)
            if quantity > 3:
                qn = round(quantity)
                qd = 1
            else:
                qn, qd = quantity.as_integer_ratio()

        db.run(f"""
        MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
        WHERE id(i)={r_id}
        SET i.name = "{name}",
        h.quantity_numerator = (CASE WHEN {qn} <> 0 THEN {qn} ELSE h.quantity_numerator END),
        h.quantity_denominator = (CASE WHEN {qd} <> 0 THEN {qd} ELSE h.quantity_denominator END),
        h.unit = (CASE WHEN "{unit}" <> "" THEN "{unit}" ELSE h.unit END)""")

        # add to clean_db_train_data
        # clean_db_train_data.append([r_name, [name, qn, qd, unit, '', '']])

merge_ingredients()

# # *** "name, preparation" format ***
print("Cleaning 'name, preparation' format...")
recipes_to_clean = db.run(r"""MATCH (i:Ingredient)
WHERE i.name =~ ".*, .*"
RETURN i.name AS name, id(i) AS id""")

for recipe in tqdm(recipes_to_clean):
    r_id = recipe['id']
    r_name = recipe['name']
    matches = re.search(r"(.*), (.*)", r_name, re.IGNORECASE)
    if matches and not ("chicken" in r_name):
        name = matches.group(1)
        prep = matches.group(2)
        # print(f"{r_name} : name={name} ; prep={prep}")
        db.run(f"""
        MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
        WHERE id(i)={r_id}
        SET i.name = "{name}",
        h.preparation = (CASE WHEN "{prep}" <> "" THEN "{prep}" ELSE h.preparation END)""")

        # add to clean_db_train_data
        # clean_db_train_data.append([r_name, [name, '', '', '', prep, '']])

merge_ingredients()

# *** separating preparation ***
# working really well
print("Separating preparations...")
recipes_to_clean = db.run(r"""
MATCH (:Recipe)-[h:HAS_INGREDIENT]->(:Ingredient)
WITH collect( distinct h.preparation) AS preps
UNWIND preps AS prep
WITH prep ORDER BY size(prep) DESC
MATCH (i:Ingredient)
WHERE i.name CONTAINS prep
RETURN i.name AS name, id(i) AS id, prep
""")

for recipe in tqdm(recipes_to_clean):
    r_id = recipe['id']
    r_name = recipe['name']
    prep = recipe['prep']
    matches = re.search(rf"(.*){re.escape(prep)}(.*)", r_name, re.IGNORECASE)
    # https://stackoverflow.com/a/55810892/14960480
    if matches:
        beginning = matches.group(1)
        end = matches.group(2)
        if beginning[-1:] == ',':
            beginning = beginning[:-1]
        if end[-1:] == ',':
            end = end[:-1]
        name = beginning + end
        # print(f"{r_name} : name={name} ; prep={prep}")
        db.run(f"""
        MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
        WHERE id(i)={r_id}
        SET i.name = "{name}",
        h.preparation = (CASE WHEN NOT exists(h.preparation) THEN "{prep}" ELSE coalesce(h.preparation,"") + ", " + "{prep}" END)
        RETURN h.preparation AS p""")

merge_ingredients()

# *** separating units ***
print("Separating units...")
recipes_to_clean = db.run(r"""
MATCH (:Recipe)-[h:HAS_INGREDIENT]->(:Ingredient)
WHERE size(h.unit)>1
WITH collect( distinct h.unit) AS units
UNWIND units AS unit
WITH unit ORDER BY size(unit) DESC
MATCH (i:Ingredient)
WHERE i.name CONTAINS unit
RETURN i.name AS name, id(i) AS id, unit
""")

for recipe in tqdm(recipes_to_clean):
    r_id = recipe['id']
    r_name = recipe['name']
    unit = recipe['unit']
    matches = re.search(rf"(.*){re.escape(unit)}(.*)", r_name, re.IGNORECASE)
    # https://stackoverflow.com/a/55810892/14960480
    if matches and "inch thick" not in r_name:
        beginning = matches.group(1)
        end = matches.group(2)
        # deals with units in the plural
        if beginning[:2] == 's ':
            beginning = beginning[2:]
        if end[:2] == 's ':
            end = end[2:]
        name = beginning + end
        # input(f"{r_name} : name={name} ; unit={unit}")
        db.run(f"""
        MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
        WHERE id(i)={r_id}
        SET i.name = "{name}",
        h.unit = (CASE WHEN NOT exists(h.unit) THEN "{unit}" ELSE coalesce(h.unit,"") + ", " + "{unit}" END)
        RETURN h.unit AS p""")

merge_ingredients()
