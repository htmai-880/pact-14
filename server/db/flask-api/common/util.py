import binascii
import os
from argon2 import PasswordHasher, exceptions
ph = PasswordHasher()

#############################   USER FUNCTIONS #####################################################

def generate_password_hash(password):
    return ph.hash(password)

def check_password_hash(hashedPassword, inputPassword):
    try:
        return ph.verify(hashedPassword, inputPassword)
    except (exceptions.VerifyMismatchError):
        return False


################################## NEO4J FUNCTIONS ####################################################
def createUser(tx, username, email, password):
    result = tx.run(
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


def get_user_by_username(tx, username):
    return tx.run(
        """
        MATCH (user:User {username: $username}) RETURN user
        """,
        {"username": username},
    ).single()

def get_user_by_email(tx, email):
    return tx.run(
        """
        MATCH (user:User {email: $email}) RETURN user
        """,
        {"email": email},
    ).single()

def get_users_by_username(tx, username):
    #TODO: Take in account created recipes
    users = []
    result = tx.run(
        """
        MATCH (user:User) WHERE user.username CONTAINS $username RETURN user
        """,
        {"username": username},
    )
    for record in result:
        users.append(record)
    return users