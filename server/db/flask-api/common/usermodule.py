from common import util


##########################################  USER CLASS  ################################################

class User():
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    def to_dict(self):
        return {"username": self.username, "email": self.email}


########################################## Exported ####################################################

def findUsersByUsername(username, driver):
    with driver.session() as session:
        users = [user.data().get("user") for user in session.read_transaction(util.get_users_by_username, username)]
        for user in users:
            user.pop('password', None)
        return users

def findUserByUsername(username, driver):
    with driver.session() as session:
        result = session.read_transaction(util.get_user_by_username, username)
        if result and result.get("user"):
            user = result.data().get("user")
            user.pop('password', None)
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
        #return the user


def registerUser(username, email, password, driver):
    if not username:
        return {'username': 'This field is required.'}, 400
    if not email:
        return {'email': 'This field is required.'}, 400
    if not password:
        return {'password': 'This field is required.'}, 400
    with driver.session() as session:
        session.write_transaction(util.create_user, username, email, password)
        print("Created user " +username +".")



########################################################################################################################
def authenticate(input_email, input_password, driver):
    user = get_user(input_email, driver)
    if user is None:
        return None
    print("There is an user with that email.")
    print(user.get("password"))
    if util.check_password_hash(user.get("password"), input_password):
        return util.User(user.get("username"), user.get("email"), user.get("password"))
    return None
    #return the User class user if auth success, None if not

def addUser(user, driver):
    registerUser(user.username, user.email, user.password, driver)

########################################################################################################################