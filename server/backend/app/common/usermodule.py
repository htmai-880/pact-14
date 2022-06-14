from . import util


##########################################  USER CLASS  ################################################

class User:
    def __init__(self, username, email, password, not_hashed=True):
        self.username = username
        self.email = email
        if not_hashed:
            self.password = util.generate_password_hash(password)
        else:
            self.password = password

    def to_dict(self):
        return {"username": self.username, "email": self.email}


########################################## Exported ####################################################

def find_users_by_username(username, driver):
    with driver.session() as session:
        users = [user.data().get("user") for user in session.read_transaction(util.get_users_by_username, username)]
        for user in users:
            user.pop('password', None)
            user.pop('api_key', None)
        return users


def findUserByUsername(username, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_user_by_username, username)
        if result and result.get("user"):
            user = result.data().get("user")
            user.pop('password', None)
            user.pop('api_key', None)
            return user
        else:
            return None


def findUserByEmail(email, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_user_by_email, email)
        if result and result.get("user"):
            user = result.data().get("user")
            user.pop('password', None)
            user.pop('api_key', None)
            return user
        else:
            return None


def isAvailableUsername(username, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_user_by_username, username)
        if result and result.get("user"):
            return False
        else:
            return True


def isAvailableEmail(email, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_user_by_email, email)
        if result and result.get("user"):
            return False
        else:
            return True


def get_user(email, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_user_by_email, email)
        print(result)
        if result is None:
            return None
        try:
            return result.get("user")
        except KeyError:
            return None
        # return the user


def registerUser(username, email, password, driver):
    with driver.session() as session:
        session.write_transaction(util.create_user, username, email, password)
        print("Created user " + username + ".")


def getUserIngredients(username, driver):
    ingredients = []
    with driver.session() as session:
        for result in session.read_transaction(util.get_user_ingredient, username):
            data = result.data()
            ingredient = data.get("i")
            ingredient["label"] = data.get("L")
            print("rel = ", data.get("rel"))
            ingredient["properties"] = {
                'unit': data.get("unit"),
                'quantity_numerator': data.get("quantity_numerator"),
                'quantity_denominator': data.get("quantity_denominator")
                }
            print("properties = ", ingredient["properties"])
            ingredient["id"] = data.get("idn")
            ingredient["own_id"] = data.get("own_id")

            ingredients.append(ingredient)
        # print("Ingredients are ", ingredients)
        return ingredients


def getUserRecipes(username, driver):
    recipes = []
    with driver.session() as session:
        for result in session.read_transaction(util.get_user_recipes, username):
            recipe = result.data().get("recipe")
            print(recipe)
            recipe["id"] = result.data().get("idn")
            print(recipe)
            recipes.append(recipe)
        return recipes


def getUserFavoriteRecipes(email, driver):
    with driver.session() as session:
        recipes = session.read_transaction(util.get_user_favorite_recipes_id, email)
        print("Recipes : ", recipes)
        return recipes


def setUserFavoriteRecipe(idn, email, driver):
    with driver.session() as session:
        session.write_transaction(util.set_user_favorite_recipe, idn, email)


def removeUserFavoriteRecipe(idn, email, driver):
    with driver.session() as session:
        session.write_transaction(util.remove_user_favorite_recipe, idn, email)


def isInFavorites(idn, email, driver):
    with driver.session() as session:
        print(session.read_transaction(util.is_in_favorites, idn, email))
        return session.read_transaction(util.is_in_favorites, idn, email) > 0


########################################################################################################################
def authenticate(input_email, input_password, driver):
    user = get_user(input_email, driver)
    if user is None:
        return None
    print("There is an user with that email.")
    print(user.get("password"))
    if util.check_password_hash(user.get("password"), input_password):
        return User(user.get("username"), user.get("email"), user.get("password"))
    return None
    # return the User class user if auth success, None if not


def addUser(user, driver):
    registerUser(user.username, user.email, user.password, driver)


def userIngredients(username, driver):
    return getUserIngredients(username, driver)


def userRecipes(username, driver):
    return getUserRecipes(username, driver)


def addIngredientForUser(ingredient_id, amount, unit, user_email, expiration_date, driver):
    with driver.session() as session:
        session.write_transaction(util.add_ingredient_for_user, ingredient_id, amount, unit, user_email, expiration_date)

def deleteIngredientForUser(own_id, user_email, driver):
    with driver.session() as session:
        session.write_transaction(util.delete_ingredient_for_user, own_id, user_email)


########################################################################################################################
def checkReqUsername(username):
    if not username:
        return False
    if " " in username:
        return False
    if "," in username:
        return False
    if "@" in username:
        return False
    if "$" in username:
        return False
    if "*" in username:
        return False
    if "=" in username:
        return False
    if "#" in username:
        return False
    return True
