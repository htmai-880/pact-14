import os
from datetime import datetime
from pathlib import Path  # Python 3.6+ only
from warnings import warn

import jwt
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Api, reqparse
# neo4j modules
from neo4j import GraphDatabase, basic_auth

from .common import recipemodule as rmod
from .common import usermodule as umod

# ------------------------------ DATA -------------------------------------------------------------

env_path = Path('.') / '.env'

if not env_path.exists():
    warn("NO .ENV !")

load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_USERNAME = os.getenv("S2R_DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("S2R_DATABASE_PASSWORD")
DATABASE_URL = os.getenv("S2R_DATABASE_URL")
CORS_HEADER = "Content-type"

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})


# -------------------------------------- Functions ----------------------------------------------------


## Actually setup the Api resource routing here
##

@app.route('/helloworld', methods=('POST',))
@cross_origin()
def HelloWorld():
    # parser = reqparse.RequestParser()
    # parser.add_argument('userdata')
    # data = parser.parse_args()
    data = request.get_json()
    print(type(data))
    print("received message: ")
    print(data)
    return {'hello': 'world'}


@app.route('/login', methods=('POST',))
@cross_origin()
def Login():
    data = request.get_json()
    print("this is the data")
    print(data)
    inputEmail = data["email"]
    print("Input Email: " + inputEmail)
    inputPassword = data["password"]
    print("Input password: " + inputPassword)

    if not inputEmail:
        return {'email': 'This field is required.'}, 400
    if not inputPassword:
        return {'password': 'This field is required.'}, 400

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    print("Connected to database successfully.")
    user = umod.authenticate(inputEmail, inputPassword, driver)
    if not user:
        return {'message': 'Invalid credentials', 'authenticated': False}, 401

    # return {'message': 'Logged in successfully', 'authenticated': True}, 200
    token = jwt.encode({
        'sub': user.email,  # The subject of the jwt, which we pick to be the email here
        'iat': datetime.utcnow(),  # Issued at present time
        'usr': user.username},  # Username
        SECRET_KEY)
    driver.close()
    return jsonify({'token': token.decode('UTF-8')}), 200


@app.route('/register', methods=('POST',))
@cross_origin()
def Register():
    data = request.get_json()

    if not data["username"]:
        return {'username': 'This field is required.'}, 400
    if not data["email"]:
        return {'email': 'This field is required.'}, 400
    if not data["password"]:
        return {'password': 'This field is required.'}, 400

    # print(data)
    inputUsername = data["username"]

    if len(inputUsername) < 3:
        return {'message': 'Provide at least 3 symbols.'}, 400
    if len(inputUsername) > 50:
        return {'message': 'Username too long. Provide less than 51 symbols'}, 400
    if not umod.checkReqUsername(inputUsername):
        return {'message': 'Username contains forbidden symbol.'}, 400

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    print("Input Username: " + inputUsername)
    if not umod.isAvailableUsername(inputUsername, driver):
        return {"message": "Username already used"}, 400

    # TODO: Verify that email is valid (confirmation mail)
    inputEmail = data["email"]
    print("Input email: " + inputEmail)
    if not umod.isAvailableEmail(inputEmail, driver):
        return {"message": "Email already used"}, 400

    # TODO: Verify that password has sufficient security

    if len(data["password"]) < 8:
        return {'message': 'Provide at least 8 symbols.'}, 400

    print("Input password: ")
    # Already hashed in constructor
    umod.addUser(umod.User(inputUsername, inputEmail, data["password"]), driver)

    driver.close()
    return {"message": "Username " + inputUsername + " registered successfully"}, 201


@app.route('/searchuser', methods=('GET',))
@cross_origin()
def SearchUser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username required')
    args = parser.parse_args()
    username = args['username']

    if len(username) < 3:
        return {'message': 'Provide at least 3 symbols.'}, 400

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    users = umod.find_users_by_username(username, driver)
    driver.close()
    if users is None:
        return {'message': 'No such user found'}, 400
    else:
        print("User is ", users)
        return {"users": users}, 200


@app.route('/userfromemail', methods=('GET',))
@cross_origin()
def UserFromMail():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email required')
    args = parser.parse_args()
    email = args["email"]
    print(email)
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    user = umod.findUserByEmail(email, driver)
    driver.close()
    if user is None:
        return {'message': 'No such user found'}, 400
    else:
        print("User is", user)
        return {"user": user}, 200


@app.route('/profile', methods=('GET',))
@cross_origin()
def Profile():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username required')
    args = parser.parse_args()
    username = args['username']

    if len(username) < 3:
        return {'message': 'Provide at least 3 symbols.'}, 400

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    user = umod.findUserByUsername(username, driver)
    driver.close()
    if user is None:
        return {'message': 'No such user found'}, 400

    print("User is ", user)
    return {"user": user}, 200


@app.route('/userrecipes', methods=('GET',))
@cross_origin()
def UserRecipes():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username required')
    args = parser.parse_args()
    username = args['username']
    if len(username) < 3:
        return {'message': 'Provide at least 3 symbols.'}, 400
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    recipes = umod.userRecipes(username, driver)
    driver.close()
    # print(username + " owns " + str(ingredients) + ".")
    return {'user_recipes': recipes}, 200


@app.route('/useringredients', methods=('GET',))
@cross_origin()
def UserIngredients():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username required')
    args = parser.parse_args()
    username = args['username']
    if len(username) < 3:
        return {'message': 'Provide at least 3 symbols.'}, 400
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    ingredients = umod.userIngredients(username, driver)
    driver.close()
    # print(username + " owns " + str(ingredients) + ".")
    return {'ingredients': ingredients}, 200


@app.route('/searchingredient', methods=('GET',))
@cross_origin()
def SearchIngredient():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Ingredient name required')
    args = parser.parse_args()
    name = args['name']

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    ingredients = rmod.findIngredientsByName(name, driver)
    driver.close()

    if ingredients is None:
        return {'message': 'No such ingredient found'}, 400

    print("Ingredient is ", ingredients)
    return {"ingredients": ingredients}, 200


@app.route('/addingredient', methods=('POST',))
@cross_origin()
def AddIngredient():
    # Adds ingredient to the database
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Ingredient name required')
    args = parser.parse_args()
    name = args['name']

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )

    if not rmod.isAvailableName(name, driver):
        return {'message': 'Ingredient with such name already exists.'}, 400

    rmod.addIngredient(name, driver)
    return {'message': 'Added ingredient to database successfully.'}, 200


@app.route('/addrecipe', methods=('POST',))
@cross_origin()
def AddRecipe():
    """parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Recipe creator email required')
    parser.add_argument('title', type=str, required=True, help='Recipe title required')
    parser.add_argument('ingredients', required=True, help='Recipe ingredients required')
    parser.add_argument('provenance', type=str)
    parser.add_argument('instructions', required=True, help='Recipe instructions required')
    args = parser.parse_args()"""
    args = request.get_json()
    email = args['email']
    title = args['title']
    print(type(args['ingredients']))
    ingredients = args['ingredients']  # This is a string converted to array
    provenance = args['provenance']
    instructions = args['instructions']

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    rmod.addRecipe(email, title, ingredients, provenance, instructions, driver)
    driver.close()

    return {'message': 'Added recipe to database successfully.'}, 200


@app.route('/searchrecipe', methods=('GET',))
@cross_origin()
def SearchRecipe():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='Recipe title required')
    args = parser.parse_args()
    title = args['title']

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    recipes = rmod.findRecipesByTitle(title, driver)
    driver.close()

    if recipes is None:
        return {'message': 'No such recipe found'}, 400

    print("Recipe is ", recipes)
    return {"recipes": recipes}, 200


@app.route('/recipe', methods=('GET',))
@cross_origin()
def Recipe():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='Recipe title required')
    args = parser.parse_args()
    title = args['title']
    title = title.replace("_", " ")
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    recipe = rmod.findRecipeByTitle(title, driver)
    driver.close()

    if recipe is None:
        return {'message': 'No such recipe found'}, 400

    print("Recipe is ", recipe.to_dict())
    return {"recipe": recipe.to_dict()}, 200


@app.route('/recipebyid', methods=('GET',))
@cross_origin()
def RecipeById():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True, help='Recipe id required')
    args = parser.parse_args()
    id = args['id']
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    recipe = rmod.findRecipeById(id, driver)
    driver.close()

    if recipe is None:
        return {'message': 'No such recipe found'}, 400

    print("Recipe is ", recipe.to_dict())
    return {"recipe": recipe.to_dict()}, 200


@app.route('/ingredient', methods=('GET',))
@cross_origin()
def Ingredient():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Ingredient name required')
    args = parser.parse_args()
    name = args['name']
    name = name.replace("_", " ")
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    ingredient = rmod.findIngredientByName(name, driver)
    driver.close()

    if ingredient is None:
        return {'message': 'No such ingredient found'}, 400

    print("Ingredient is ", ingredient)
    return {"ingredient": ingredient}, 200

@app.route('/getallingredientswithunit', methods=('GET',))
@cross_origin()
def GetAllIngredientsWithUnit():
    """returns all ingredients with ONLY ONE VALID UNIT FOR THIS ingredient"""
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    ingredients = rmod.getAllIngredientsWithUnit(driver)
    driver.close()

    print(f"Number of ingredients {len(ingredients)}")
    return {"ingredients": ingredients}, 200


@app.route('/getallingredientswithunits', methods=('GET',))
@cross_origin()
def GetAllIngredientsWithUnits():
    """returns all ingredients with all valid units for this ingredient"""
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    ingredients = rmod.getAllIngredientsWithUnits(driver)
    driver.close()

    print(f"Number of ingredients {len(ingredients)}")
    return {"ingredients": ingredients}, 200


@app.route('/getunitforingredient', methods=('GET',))
@cross_origin()
def GetUnitForIngredient():
    """returns unit for one ingredient by id"""
    parser = reqparse.RequestParser()
    parser.add_argument('ingredient_id', type=int, required=False, help='Ingredient name or id required')
    parser.add_argument('ingredient_name', type=str, required=False, help='Ingredient name or id required')
    args = parser.parse_args()
    ingredient_id = args['ingredient_id']
    ingredient_name = args['ingredient_name']

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    if ingredient_id is None and ingredient_name is None:
        return 400
    elif ingredient_id is not None:
        unit = rmod.getUnitForIngredientById(ingredient_id, driver)
    else:
        unit = rmod.getUnitForIngredientByName(ingredient_name, driver)
    driver.close()

    print("Unit ", unit)
    return {"unit": unit}, 200


@app.route('/getunitsforingredient', methods=('GET',))
@cross_origin()
def GetUnitsForIngredient():
    """returns all possible units for one ingredient by id"""
    parser = reqparse.RequestParser()
    parser.add_argument('ingredient_id', type=int, required=True, help='Ingredient id required')
    args = parser.parse_args()
    ingredient_id = args['ingredient_id']

    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    units = rmod.getUnitsForIngredient(ingredient_id, driver)
    driver.close()

    print("units are ", units)
    return {"units": units}, 200


@app.route('/addingredientforuser', methods=('POST','DELETE'))
@cross_origin()
def AddIngredientForUser():
    if request.method == 'POST':
        """add an ingredient to an user fridge by id"""
        parser = reqparse.RequestParser()
        parser.add_argument('ingredient_id', type=int, required=True, help='Ingredient id required')
        parser.add_argument('amount', type=int, required=True, help='amount, required (ex : "1" apple)')
        parser.add_argument('unit', type=str, required=True, help='unit (ex : "gr", "L")')
        # parser.add_argument('user_id', type=int, required=False, help='User id')
        parser.add_argument('expiration_date', type=str, required=False, help="Expiration date ex:'2015-07-21'")
        parser.add_argument('user_email', type=str, required=True, help='User email, required')
        args = parser.parse_args()
        print(args)
        ingredient_id = args['ingredient_id']
        amount = args['amount']
        unit = args['unit']
        # user_id = args['user_id']
        expiration_date = args['expiration_date']
        user_email = args['user_email']
        # todo : use user_email

        driver = GraphDatabase.driver(
            DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
        )
        umod.addIngredientForUser(ingredient_id, amount, unit, user_email, expiration_date, driver)
        driver.close()

        print(f"user {user_email} has {amount}{unit} new ingredient {ingredient_id}")
        return jsonify({'message': 'OK'}), 200

    if request.method == 'DELETE':
        parser = reqparse.RequestParser()
        parser.add_argument('own_id', type=int, required=True, help='ID of the ownership relation, required')
        parser.add_argument('user_email', type=str, required=True, help='User email, required')
        args = parser.parse_args()
        user_email = args['user_email']
        own_id = args['own_id']
        print(args)
        driver = GraphDatabase.driver(
            DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
        )
        umod.deleteIngredientForUser(own_id, user_email, driver)
        driver.close()

        return jsonify({'message': 'Delete OK for relation' + str(own_id)})


@app.route('/getallingredients', methods=('POST',))
@cross_origin()
def GetAllIngredients():
    """returns all ingredients from the database"""
    driver = GraphDatabase.driver(
        DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
    )
    ingredients = rmod.getAllIngredients(driver)
    driver.close()

    print(f"Number of ingredients {len(ingredients)}")
    return {"ingredients": ingredients}, 200

@app.route('/favorite', methods=('GET', 'POST',))
@cross_origin()
def UserFavorite():
    print("User favorite: ")
    if request.method == 'POST':
        print("POST")
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_id', type=int, required=True, help='Recipe id required')
        parser.add_argument('email', type=str, required=True, help='User email, required')

        args = parser.parse_args()

        idn = args['recipe_id']
        email = args['email']
        print(email)
        driver = GraphDatabase.driver(
            DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
        )
        print("Placeholder function to add/remove recipe " + str(idn) + " to user " + email + "favorites.")

        if umod.isInFavorites(idn, email, driver):
            print("Recipe is in favorites. Removing it from favorites.")
            umod.removeUserFavoriteRecipe(idn, email, driver)
        else:
            print("Recipe is not in favorites. Setting it in favorites.")
            umod.setUserFavoriteRecipe(idn, email, driver)
        driver.close()

        return jsonify({"message": "Successfully added/removed recipe " + str(idn) + " to favorites for user " + email + "."}), 200


    elif request.method == 'GET':
        print("GET")
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='User email, required')

        args = parser.parse_args()

        email = args['email']
        print(email)
        driver = GraphDatabase.driver(
            DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
        )
        print("Placeholder function to get recipes in user " + email + "favorites.")
        recipes_liked_by_user = umod.getUserFavoriteRecipes(email, driver)
        driver.close()

        return jsonify({"recipes": recipes_liked_by_user}), 200
        
@app.route('/rating', methods=('GET', 'POST',))
@cross_origin()
def Rating():
    if request.method == 'POST':
        print("POST")
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_id', type=int, required=True, help='Recipe id required')
        parser.add_argument('email', type=str, required=True, help='User email, required')
        parser.add_argument('rating_grade', type=int, required=True, help='Grade of recipe required, integer from 1 to 5')
        parser.add_argument('rating_comment', type=str, required=True, help='Comment of recipe required, string')

        args = parser.parse_args()
        print(args)
        idn = args['recipe_id']
        email = args['email']
        grade = args['rating_grade']
        comment = args['rating_comment']

        driver = GraphDatabase.driver(
            DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
        )
        print("function to POST user "+ email + " rating to recipe " + str(idn))
        rmod.postRecipeRatings(idn, email, grade, comment, driver)
        driver.close()

        return jsonify({'message': "Successfully added user "+ email + " rating to recipe " + str(idn)}),200

    elif request.method == 'GET':
        print("GET")
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_id', type=int, required=True, help='Recipe id required')
        args = parser.parse_args()
        idn = args['recipe_id']
        driver = GraphDatabase.driver(
            DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
        )
        print("function to GET ratings of recipe " + str(idn))
        ratings = rmod.getRecipeRatings(idn, driver)
        driver.close()
        return jsonify({'ratings': ratings}), 200


def main():
    app.run(host="0.0.0.0", port=80)
    # app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == '__main__':
    main()
