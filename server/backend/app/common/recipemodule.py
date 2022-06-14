from . import util


# ----------------------------------  RECIPE CLASS  ------------------------------------------------------
class Ingredient:
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties

    def to_dict(self):
        return {"name": self.name, "properties": self.properties}

    def __repr__(self):
        return str(self.to_dict())


class Recipe:
    def __init__(self, title, ingredients, instructions, provenance=None, idn=0):
        self.title = title
        self.ingredients = ingredients  # list of ingredients
        self.instructions = instructions
        self.provenance = provenance
        self.id = idn

    def to_dict(self):
        liste = [x.to_dict() for x in self.ingredients]
        return {"title": self.title, "ingredients": liste, "instructions": self.instructions,
                "provenance": self.provenance, "id": self.id}

    def __repr__(self):
        return str(self.to_dict())


# ----------------------------------    RECIPE FUNCTIONS --------------------------------------------------

def isAvailableName(name, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_ingredients, name)
        if result and len(result) > 0:
            return False
        else:
            return True


def findIngredientsByName(name, driver):
    print("Name: ", name)
    with driver.session() as session:
        ingredients = []
        for ing in session.read_transaction(util.get_ingredients, name):
            d = ing.data().get("i")
            d["id"] = ing.data().get("id")
            ingredients.append(d)
        return ingredients

def findIngredientByName(name, driver):
    # print("placeholder function to find ingredient")
    with driver.session() as session:
        ingredient = session.read_transaction(util.get_ingredient, name)
        returned_ingredient = ingredient.get("i")
        returned_ingredient["id"] = ingredient.get("id")
        return returned_ingredient

def addIngredient(name, driver):
    with driver.session() as session:
        session.write_transaction(util.add_ingredient, name)
        print("Created ingredient " + name + ".")


def addRecipe(email, title, ingredients, provenance, instructions, driver):
    args = {
        'email': email,
        'title': title,
        'ingredients': ingredients,
        'provenance': provenance,
        'instructions': instructions
    }
    print(args)
    with driver.session() as session:
        session.write_transaction(util.add_recipe, args)
        print("User " + email + "created recipe " + title + ".")


def isAvailableTitle(title, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_recipe, title)
        if result and len(result) > 0:
            return False
        else:
            return True


def findRecipesByTitle(title, driver):
    print("Title: ", title)
    with driver.session() as session:
        recipes = []
        for recipe in session.read_transaction(util.get_recipe, title):
            entry = recipe.data().get("r")
            entry["id"] = recipe.data().get("idn")
            recipes.append(entry)
        return recipes


def getIngredientsOfRecipe(title, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_ingredients_of_recipe, title)
        # print("Result = ", result)
        L = [ingredient.items() for ingredient in result]

        ingredients = []  # List of ingredient class objects

        for element in L:
            #     print(dict(element[0][1].items()))  # ingredient
            #     print(dict(element[1][1].items()))  #properties

            ingredients.append(Ingredient(dict(element[0][1].items()).get('name'), dict(element[1][1].items())))
        print("Ingredients = ", ingredients)
        recipe_dict = dict(element[2][1].items())  # Recipe information
        recipe_dict["Idn"] = element[3][1]
        print("Recipe dict = ", recipe_dict)
        return recipe_dict, ingredients


def findRecipeByTitle(title, driver):  # find a recipe with its ingredients and their properties
    r, ingredients = getIngredientsOfRecipe(title, driver)
    print("r=", r)
    recipe = Recipe(r.get("title"), ingredients, r.get("instructions"), r.get("provenance"), r.get("Idn"))
    print("Recipe: ", recipe)
    return recipe


def getIngredientsOfRecipeById(r_id, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_ingredients_of_recipe_by_title, r_id)
        # print("Result = ", result)
        liste = [ingredient.items() for ingredient in result]

        ingredients = []  # List of ingredient class objects

        for element in liste:
            #     print(dict(element[0][1].items()))  # ingredient
            #     print(dict(element[1][1].items()))  #properties

            ingredients.append(Ingredient(dict(element[0][1].items()).get('name'), dict(element[1][1].items())))
        print("Ingredients = ", ingredients)
        recipe_dict = dict(element[2][1].items())  # Recipe information
        recipe_dict["Idn"] = element[3][1]
        print("Recipe dict = ", recipe_dict)
        return recipe_dict, ingredients


def findRecipeById(r_id, driver):
    r, ingredients = getIngredientsOfRecipeById(r_id, driver)
    instructions_list = r.get("instructions")
    if (type(instructions_list)==list):
        recipe = Recipe(r.get("title"), ingredients, instructions_list, r.get("provenance"), r.get("Idn"))
        print("Recipe: ", recipe)
        return recipe
    else:
        instructions_list = list(filter(None, instructions_list.replace(". ", ". \n").split('\n')))
        recipe = Recipe(r.get("title"), ingredients, instructions_list, r.get("provenance"), r.get("Idn"))
        print("Recipe: ", recipe)
        return recipe

def getRecipeRatings(r_id, driver):
    with driver.session() as session:
        ratings = session.read_transaction(util.get_recipe_ratings, r_id)
        print(ratings)
    return ratings

def postRecipeRatings(r_id, email, grade, comment, driver):
    with driver.session() as session:
        session.write_transaction(util.post_recipe_rating, r_id, email, grade, comment)

def getAllIngredientsWithUnits(driver):
    """get all possibles ingredients with all possibles units"""
    with driver.session() as session:
        ingredients = session.read_transaction(util.get_all_ingredients_with_units)
    return ingredients


def getAllIngredientsWithUnit(driver):
    """get all possibles ingredients with ONLY ONE unit"""
    ingredients = getAllIngredientsWithUnits(driver)
    if len(ingredients):
        return ingredients[0]
    return None


def getUnitsForIngredient(i_id, driver):
    """get all possibles units for an ingredient, by id"""
    with driver.session() as session:
        ingredients = session.read_transaction(util.get_units_for_ingredient, i_id)
        print(ingredients)
        return ingredients


def getUnitForIngredientById(i_id, driver):
    """get ONLY ONE unit for an ingredient, by id"""
    res = getUnitsForIngredient(i_id, driver)
    if len(res):
        return res[0]["units"]
    return None


def getUnitsForIngredientByName(i_id, driver):
    """get all possibles units for an ingredient, by id"""
    with driver.session() as session:
        ingredients = session.read_transaction(util.get_units_for_ingredient_by_name, i_id)
        print(ingredients)
        return ingredients


def getUnitForIngredientByName(name, driver):
    """get ONLY ONE unit for an ingredient, by name"""
    res = getUnitsForIngredientByName(name, driver)
    if len(res):
        return res[0]["units"]
    return None


def getAllIngredients(driver):
    """get all ingredients"""
    ingredients = getAllIngredients(driver)
    return ingredients
