import time

from server.ai.app.ai.db import DB
from server.ai.app.ai.main import get_recipe
from os import environ

from server.ai.app.common.ingredient import Ingredient

environ["DB_URL"] = "bolt://localhost:11003"
environ["DB_USER"] = "neo4j"
environ["DB_PASS"] = "pact2020"

db = DB()




user_ings_names = ["salt", "white sugar", "all-purpose flour", "butter", "water", "olive oil", "milk", "egg", "lemon juice", "mayonnaise", "honey", "paprika", "margarine", "orange juice", "slices bacon", "Dijon mustard", "pepper", "rice", "onion", "mushrooms"]

print("User ingredients :")
print(""" "salt", "white sugar", "all-purpose flour", "butter", "water", "olive oil", "milk", "egg", "lemon juice", "mayonnaise", "honey", "paprika", "margarine", "orange juice", "slices bacon", "Dijon mustard", "pepper", "rice", "onion", "mushrooms" """)
input("ENTER to continue")
print("OBSOLETE : USE USER EMAIL")
exit()
user_ingredients = [Ingredient(id=x['id'], amount=1, unit="") for x in db.run(f"MATCH (i:Ingredient) WHERE i.name IN {user_ings_names} RETURN id(i) AS id")]

print("Possible recipes (limit 10) :")
recipes = get_recipe(user_ingredients, limit=10)
recipes_desc = db.run(f"""MATCH (r:Recipe) WHERE id(r) IN {recipes}
                        WITH r
                        MATCH (r)-[:HAS_INGREDIENT]->(i:Ingredient)
                        WITH r, collect(i.name) AS ingredients
                        RETURN r.title AS title, r.instructions AS instruct, ingredients, labels(r) AS labels""")
for r in recipes_desc:
    mention = ' (Created by AI)' if 'CreatedByAI' in r['labels'] else ''
    print(f"# {r['title']}{mention}")
    print(r['ingredients'])
    print(r['instruct'].replace(". ", "\n. "))
input("ENTER to continue")
print()

for i in range(1, 10):
    recipes = [x['id'] for x in get_recipe(user_ingredients, limit=5, startsfrom=i*5)]
    recipes_desc = db.run(f"""MATCH (r:Recipe) WHERE id(r) IN {recipes}
                            RETURN r.title AS title, labels(r) AS labels""")
    for r in recipes_desc:
        mention = ' (Created by AI)' if 'CreatedByAI' in r['labels'] else ''
        print(f"# {r['title']}{mention}")
    time.sleep(1)
    print()
