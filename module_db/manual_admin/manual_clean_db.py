from server.ai.app.ai.db import DB
import pickle
import atexit


# function is executed before script terminates
def exit_handler():
    with open("clean_db_train_data.pickle", "wb") as output_file:
        pickle.dump(clean_db_train_data, output_file)


atexit.register(exit_handler)

try:
    with open("clean_db_train_data.pickle", "rb") as input_file:
        clean_db_train_data = pickle.load(input_file)
except FileNotFoundError:
    clean_db_train_data = []

db = DB()

# clean little used recipes with 99% true positive
# recipes_to_clean = db.run("""
# MATCH (i:Ingredient)
# WHERE size(split(i.name,' ')) > 2
# RETURN id(i) AS id, i.name AS name
# ORDER BY size((i)<-[:HAS_INGREDIENT]-(:Recipe))
# LIMIT 50""")

# clean heavily used ingredients with 90% FALSE positive
recipes_to_clean = db.run("""
MATCH (i:Ingredient)
WHERE size(split(i.name,' ')) > 3 AND NOT i:ManuallyVerified
RETURN id(i) AS id, i.name AS name
ORDER BY size((i)<-[:HAS_INGREDIENT]-(:Recipe)) DESC
LIMIT 100""")

for recipe in recipes_to_clean:
    r_id = recipe['id']
    r_name = recipe['name']
    print(r_name)
    name = input("ingredient name : ").strip()
    if name:
        qn = input("quantity_numerator : ").strip()
        qd = input("quantity_denominator : ").strip()
        unit = input("unit : ").strip()
        preparation = input("preparation : ").strip()
        opt = input("optional : ").strip()
    else:
        # nothing to change
        name = r_name
        qn = 0
        qd = 0
        unit = ''
        preparation = ''
        opt = ''

    # optional => true/false
    optional = opt == "t" or opt == "o" or opt == "T" or opt == "O"
    # convert quantities to int
    try:
        qn = int(qn)
        qd = int(qd)
    except ValueError:
        qn = 0
        qd = 0

    # modify ingredient name, recipes amount, etc.
    print(r_id)
    db.run(f"""
    MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
    WHERE id(i)={r_id}
    SET i.name = "{name}", i:ManuallyVerified,
    h.quantity_numerator = (CASE WHEN {qn} <> 0 THEN {qn} ELSE h.quantity_numerator END),
    h.quantity_denominator = (CASE WHEN {qd} <> 0 THEN {qd} ELSE h.quantity_denominator END),
    h.unit = (CASE WHEN "{unit}" <> "" THEN "{unit}" ELSE h.unit END),
    h.preparation = (CASE WHEN "{preparation}" <> "" THEN "{preparation}" ELSE h.preparation END),
    h.option = {optional}""")

    print()

    # add to clean_db_train_data
    clean_db_train_data.append([r_name, [name, qn, qd, unit, preparation, opt]])
