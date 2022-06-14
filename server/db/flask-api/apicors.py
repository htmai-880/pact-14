from flask import Flask, request, jsonify
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin
import jwt
from datetime import datetime, timedelta

import os
from pathlib import Path  # Python 3.6+ only
from common import usermodule as umod

# neo4j modules
from neo4j import GraphDatabase, basic_auth
from dotenv import load_dotenv

# ------------------------------ DATA -------------------------------------------------------------

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_USERNAME = os.getenv("S2R_DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("S2R_DATABASE_PASSWORD")
DATABASE_URL = os.getenv("S2R_DATABASE_URL")
CORS_HEADER = "Content-type"

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})


############################## Functions ###############################################


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

    user = umod.authenticate(inputEmail, inputPassword, driver)
    if not user:
        return {'message': 'Invalid credentials', 'authenticated': False}, 401

    # return {'message': 'Logged in successfully', 'authenticated': True}, 200
    token = jwt.encode({
        'sub': user.email,  # The subject of the jwt, which we pick to be the email here
        'iat': datetime.utcnow(),  # Issued at present time
        'exp': datetime.utcnow() + timedelta(minutes=20)},  # Expires in 20 minutes
        SECRET_KEY)
    driver.close()
    return jsonify({'token': token.decode('UTF-8')}), 200


@app.route('/register', methods=('POST',))
@cross_origin()
def Register():
    data = request.get_json()
    # print(data)
    # TODO: Verify that username does not contain invalid characters
    inputUsername = data["username"]

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
    users = umod.findUsersByUsername(username, driver)
    driver.close()
    if users is None:
        return {'message': 'No such user found'}, 400
    else:
        print("User is ", users)
        return {"users": users}, 200


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


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
