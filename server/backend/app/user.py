import binascii
import os

from argon2 import PasswordHasher

from .common import util

ph = PasswordHasher()


#############################   USER CLASS FUNCTIONS #####################################################

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = util.generate_password_hash(password)

    def to_dict(self):
        return {"username": self.username, "email": self.email}


################################## NEO4J FUNCTIONS ####################################################
def createUser(tx, username, email, password):
    tx.run(
        '''
        CREATE (user:User {username: $username, email: $email,
                           password: $password,
                           api_key: $api_key}) RETURN user
        ''',
        username=username,
        email=email,
        password=password,
        api_key=binascii.hexlify(os.urandom(20)).decode()
    )


########################################## Exported ####################################################

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
    if not username:
        return {'username': 'This field is required.'}, 400
    if not email:
        return {'email': 'This field is required.'}, 400
    if not password:
        return {'password': 'This field is required.'}, 400
    with driver.session() as session:
        session.write_transaction(util.createUser, username, email, password)
        print("Created user " + username + ".")


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
