import os
from pathlib import Path  # Python 3.6+ only
from warnings import warn

from dotenv import load_dotenv
from neo4j import GraphDatabase

from common import usermodule as umod

# --------------------------    DATABASE CREDENTIALS    -----------------------------------
env_path = Path('..') / '.env'

if not env_path.exists():
    warn("NO .ENV !")

load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_USERNAME = os.getenv("S2R_DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("S2R_DATABASE_PASSWORD")
DATABASE_URL = os.getenv("S2R_DATABASE_URL")

# --------------------------    DATA    ---------------------------------

USERS = [
    {'username': 'Rion', 'email': 'rion@example.com', 'password': 'badpassword0'},
    {'username': 'John', 'email': 'john@example.com', 'password': 'badpassword1'},
    {'username': 'Arthur', 'email': 'arthur@example.com', 'password': 'badpassword2'},
    {'username': 'Noelle', 'email': 'noelle@example.com', 'password': 'badpassword3'},
    {'username': 'Mayu', 'email': 'mayu@example.com', 'password': 'badpassword2'},
    {'username': 'Noel', 'email': 'noel@example.com', 'password': 'badpassword3'}
]

INGREDIENTS = [
    {'name': 'Soy sauce'},
    {'name': 'Mayonnaise'},
    {'name': 'Ketchup'},
    {'name': 'Guacamole'},
    {'name': 'Tabasco'},
    {'name': 'Yogurt'},
]

RECIPES = [
    {'title': "Cursed dip", 'instructions': ['Mix everything.', 'Serve.'], 'provenance': "Rion's deadly recipes"},
    {'title': "Blessed dip", 'instructions': ['Mix everything at once.', 'Eat.', 'Perish.'],
     'provenance': "Rion's deadly recipes"}
]

driver = GraphDatabase.driver(
    DATABASE_URL, auth=(DATABASE_USERNAME, DATABASE_PASSWORD)
)


# -------------------------    CLEAR DATABASE    ---------------------------------

def clear_db(tx):
    tx.run("MATCH(n) DETACH DELETE(n)")


with driver.session() as session:
    session.write_transaction(clear_db)

# -------------------------    INITIALIZE USERS    --------------------------------

for user in USERS:
    umod.addUser(umod.User(user["username"], user["email"], user["password"]), driver)


# -------------------------    INITIALIZE INGREDIENTS AND RECIPE    --------------------------------

def create_recipe(tx, recipe):
    tx.run(
        '''
        MERGE (r:Recipe {title: $title, instructions: $instructions, provenance: $provenance})
        ''',
        recipe
    )


def recipe_creator(tx, recipe, creator):
    tx.run(
        '''
        MATCH (r:Recipe {title: $title})
        MATCH (u:User {username: $username})
        MERGE (u)-[:CREATED]->(r)
        ''',
        {
            "title": recipe.get("title"),
            "username": creator
        }
    )


def create_ingredient(tx, ingredient):
    tx.run(
        '''
        MERGE (ing:Ingredient {name: $name})
        ''',
        {"name": ingredient.get("name")}
    )


def add_ingredient(tx, recipe, ingredient):
    tx.run(
        '''
        MATCH (r:Recipe {title: $title})
        MATCH (ing:Ingredient {name: $name})
        MERGE (r)-[:HAS_INGREDIENT {quantity_numerator:1, quantity_denominator:2, preparation:'prep', unit:'gr'}]->(ing)
        ''',
        {
            "title": recipe.get("title"),
            "name": ingredient.get("name")
        }
    )


def user_owns(tx, username, ingredient):
    tx.run(
        '''
        MATCH (u:User {username: $username}) MATCH (i:Ingredient {name: $name})
        CREATE (u)-[:OWNS_INGREDIENT {quantity_numerator:1, quantity_denominator:2, unit:'gr'}]->(i)
        ''',
        {
            "username": username,
            "name": ingredient.get("name")
        }
    )


with driver.session() as session:
    session.write_transaction(create_recipe, RECIPES[0])
    session.write_transaction(recipe_creator, RECIPES[0], "Rion")
    for i in range(len(INGREDIENTS)):
        session.write_transaction(create_ingredient, INGREDIENTS[i])

with driver.session() as session:
    session.write_transaction(create_recipe, RECIPES[0])
    for i in range(5):
        session.write_transaction(add_ingredient, RECIPES[0], INGREDIENTS[i])
        session.write_transaction(user_owns, "Arthur", INGREDIENTS[i])

with driver.session() as session:
    session.write_transaction(create_recipe, RECIPES[1])
    session.write_transaction(recipe_creator, RECIPES[1], "Rion")
    for i in range(2, len(INGREDIENTS)):
        session.write_transaction(add_ingredient, RECIPES[1], INGREDIENTS[i])
        session.write_transaction(user_owns, "Noelle", INGREDIENTS[i])

# -------------------------    INITIALIZE RELATIONSHIPS    --------------------------------

driver.close()
