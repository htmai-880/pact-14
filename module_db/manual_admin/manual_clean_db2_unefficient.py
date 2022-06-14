from server.ai.app.ai.db import DB
import pickle
import atexit

# FONCTIONNE, MAIS TRES PEU EFFICACE

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

# DB_PASS=pact2020;DB_USER=neo4j;DB_URL=bolt://localhost:11003
db = DB()

# clean
recipes_to_clean = db.run("""
MATCH (i:Ingredient), (ii:Ingredient)
WHERE i.name CONTAINS " "+ii.name+" "
RETURN i.name AS long, ii.name AS short LIMIT 100""")

for recipe in recipes_to_clean:
    r_long = recipe['long']
    r_short = recipe['short']
    print(f'{r_long} => {r_short}')
    name = input("ingredient name : ").strip()
    if name:
        qn = input("quantity_numerator : ").strip()
        qd = input("quantity_denominator : ").strip()
        unit = input("unit : ").strip()
        preparation = input("preparation : ").strip()
        opt = input("optional : ").strip()
    else:
        # nothing to change
        name = r_long
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
    db.run(f"""
    MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
    WHERE i.name="{r_long}"
    SET i.name = "{name}", i:ManuallyVerified,
    h.quantity_numerator = (CASE WHEN {qn} <> 0 THEN {qn} ELSE h.quantity_numerator END),
    h.quantity_denominator = (CASE WHEN {qd} <> 0 THEN {qd} ELSE h.quantity_denominator END),
    h.unit = (CASE WHEN "{unit}" <> "" THEN "{unit}" ELSE h.unit END),
    h.preparation = (CASE WHEN "{preparation}" <> "" THEN "{preparation}" ELSE h.preparation END),
    h.option = {optional}""")

    print()

    # add to clean_db_train_data
    clean_db_train_data.append([r_long, [name, qn, qd, unit, preparation, opt]])
