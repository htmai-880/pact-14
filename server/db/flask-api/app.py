import binascii
import hashlib
import os
import ast
import re
import sys
import uuid
from dotenv import load_dotenv, find_dotenv
from functools import wraps

from flask import Flask, g, request, abort, request_started
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_json import FlaskJSON, json_response

from neo4j import GraphDatabase, basic_auth

from argon2 import PasswordHasher

from user import get_user


ph = PasswordHasher()

# Source: neo4j Developer

#############################################################################################################   TODO: CODE INCOMPLET

app = Flask(__name__)
load_dotenv(find_dotenv())

app = Flask(__name__)

CORS(app)
FlaskJSON(app)

api = Api(app, title="Neo4j Movie Demo API", api_version="0.0.10")


@api.representation("application/json")
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)


def env(key, default=None, required=True):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError("Missing required environment variable '%s'" % key)


DATABASE_USERNAME = env("S2R_DATABASE_USERNAME")
DATABASE_PASSWORD = env("S2R_DATABASE_PASSWORD")
DATABASE_URL = env("S2R_DATABASE_URL")

driver = GraphDatabase.driver(
    DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
)
app.config["SECRET_KEY"] = env("SECRET_KEY")


#################################################   Functions


def get_db():
    if not hasattr(g, "neo4j_db"):
        g.neo4j_db = driver.session()
    return g.neo4j_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "neo4j_db"):
        g.neo4j_db.close()


def set_user(sender, **extra):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        g.user = {"id": None}
        return
    match = re.match(r"^Token (\S+)", auth_header)
    if not match:
        abort(401, "invalid authorization format. Follow `Token <token>`")
        return
    token = match.group(1)

    def get_user_by_token(tx, token):
        return tx.run(
            """
            MATCH (user:User {api_key: $api_key}) RETURN user
            """,
            {"api_key": token},
        ).single()

    db = get_db()
    result = db.read_transaction(get_user_by_token, token)
    try:
        g.user = result["user"]
    except (KeyError, TypeError):
        abort(401, "invalid authorization key")
    return


request_started.connect(set_user, app)


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"message": "no authorization provided"}, 401
        return f(*args, **kwargs)

    return wrapped


##################################################  User Model  ###################################################


def serialize_user(user):
    return {
        "id": user["id"],
        "username": user["username"],
        "avatar": {
            "full_size": "https://www.gravatar.com/avatar/{}?d=retro".format(
                hash_avatar(user["username"])
            )  # Change link
        },
    }


################################################## Hash functions   #############################################
############################### TODO: Change hash functions to argon2 instead of sha256
def hash_password(username, password):
    return ph.hash(password)


def match_password(hashed_pw, input_pw):
    return ph.verify(hashed_pw, input_pw)


def hash_avatar(username):
    """

    :param username:
    :return:
    """
    if sys.version[0] == 2:
        s = username
    else:
        s = username.encode("utf-8")
    return hashlib.md5(s).hexdigest()


##################################################  Classes  ####################################################


class User(Resource):
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    # The way a user is printed
    def __repr__(self):
        return f"<User: {self.username}"


class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username:
            return {"username": "This field is required."}, 400
        if not password:
            return {"password": "This field is required."}, 400

        def get_user_by_username(tx, username):
            return tx.run(
                """
                MATCH (user:User {username: $username}) RETURN user
                """,
                {"username": username},
            ).single()

        db = get_db()
        result = db.read_transaction(get_user_by_username, username)
        if result and result.get("user"):
            return {"username": "username already in use"}, 400

        def create_user(tx, username, password):
            return tx.run(
                """
                CREATE (user:User {id: $id, username: $username, password: $password, api_key: $api_key}) RETURN user
                """,
                {
                    "id": str(uuid.uuid4()),
                    "username": username,
                    "password": hash_password(username, password),
                    "api_key": binascii.hexlify(os.urandom(20)).decode(),
                },
            ).single()

        results = db.write_transaction(create_user, username, password)
        user = results["user"]
        return serialize_user(user), 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username:
            return {"username": "This field is required."}, 400
        if not password:
            return {"password": "This field is required."}, 400

        user = get_user(get_db(), username)
        if user is None:
            return {"username": "username does not exist"}, 400

        if match_password(user["password"], password):
            return {"token": user["api_key"]}

        return {"password": "wrong password"}, 400


class UserMe(Resource):
    @login_required
    def get(self):
        return serialize_user(g.user)


class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username:
            return {"username": "This field is required."}, 400
        if not password:
            return {"password": "This field is required."}, 400

        def get_user_by_username(tx, username):
            return tx.run(
                """
                MATCH (user:User {username: $username}) RETURN user
                """,
                {"username": username},
            ).single()

        db = get_db()
        result = db.read_transaction(get_user_by_username, username)
        if result and result.get("user"):
            return {"username": "username already in use"}, 400

        def create_user(tx, username, password):
            return tx.run(
                """
                CREATE (user:User {id: $id, username: $username, password: $password, api_key: $api_key}) RETURN user
                """,
                {
                    "id": str(uuid.uuid4()),
                    "username": username,
                    "password": hash_password(username, password),
                    "api_key": binascii.hexlify(os.urandom(20)).decode(),
                },
            ).single()

        results = db.write_transaction(create_user, username, password)
        user = results["user"]
        return serialize_user(user), 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username:
            return {"username": "This field is required."}, 400
        if not password:
            return {"password": "This field is required."}, 400

        def get_user_by_username(tx, username):
            return tx.run(
                """
                MATCH (user:User {username: $username}) RETURN user
                """,
                {"username": username},
            ).single()

        db = get_db()
        result = db.read_transaction(get_user_by_username, username)
        try:
            user = result["user"]
        except KeyError:
            return {"username": "username does not exist"}, 400

        expected_password = hash_password(user["username"], password)
        if user["password"] != expected_password:
            return {"password": "wrong password"}, 400
        return {"token": user["api_key"]}


class UserMe(Resource):
    @login_required
    def get(self):
        return serialize_user(g.user)


# def attempt_connection(username, password):
#     neo4j_import_thread.join()
#     # wait for neo4j to be loaded
#     # noinspection PyGlobalUndefined
#     if graph.run("""MATCH (u:User {{user_name:"{}"}}) RETURN count(u) AS c""".format(username)).data()[0]['c'] == 0:
#         print("Ce nom d'utilisateur n'existe pas.")
#         return False
#         # Effacer l'entrée de nom d'utilisateur
#
#     else:
#         # Check if password matches
#         try:
#             # Retrieved hashed password from database
#             password_hash = graph.run('MATCH (u:user {user_name:"' + username + '"}) RETURN u.user_hashed_pw AS h').data()[0]['h']
#
#             if ph.verify(password_hash, password):
#                 # check the hash's parameters and if outdated, rehash the user's password in the database.
#                 if ph.check_needs_rehash(password_hash):
#                     graph.run('MATCH (u:user {user_name:"' + username + '"}) SET u.user_hashed_pw="' + ph.hash(password) + '"')
#
#                 # Allow connection
#                 print("Connected.")
#                 return True
#
#         except VerifyMismatchError:
#             # Si le mot de passe n'est pas le bon.
#             print('Mauvais mot de passe.')
#             Return False
