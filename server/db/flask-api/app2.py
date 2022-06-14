from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import jwt
from datetime import datetime, timedelta

import os
from pathlib import Path  # Python 3.6+ only
from user import User, isAvailableUsername, isAvailableEmail, authenticate, addUser

# neo4j modules
from neo4j import GraphDatabase, basic_auth
from dotenv import load_dotenv

####################################### DATA ################################################

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_USERNAME = os.getenv("S2R_DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("S2R_DATABASE_PASSWORD")
DATABASE_URL = os.getenv("S2R_DATABASE_URL")

app = Flask(__name__)
api = Api(app)


'''
login_fields = {
    'login_attempt': fields.String
}

register_fields = {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
}'''


############################## Functions ###############################################




## Actually setup the Api resource routing here
##

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}, 200

class Login(Resource):
    def get(self):
        data = request.get_json()
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

        user = authenticate(inputEmail, inputPassword, driver)
        if not user:
            return {'message': 'Invalid credentials', 'authenticated': False}, 401

        #return {'message': 'Logged in successfully', 'authenticated': True}, 200
        token = jwt.encode({
            'sub': user.email, #The subject of the jwt, which we pick to be the email here
            'iat': datetime.utcnow(), #Issued at present time
            'exp': datetime.utcnow() + timedelta(minutes=20)}, #Expires in 20 minutes
            SECRET_KEY)
        driver.close()
        return jsonify({'token': token.decode('UTF-8')}), 200


class Register(Resource):
    def post(self):
        data = request.get_json()
        inputUsername = data["username"]


        driver = GraphDatabase.driver(
            DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
        )
        print("Input Username: " + inputUsername)
        if not isAvailableUsername(inputUsername, driver):
            return {"message": "Username already used"}, 400

        inputEmail = data["email"]
        print("Input email: " + inputEmail)
        if not isAvailableEmail(inputEmail, driver):
            return {"message": "Email already used"}, 400

        inputPassword = data["password"]
        print("Input password: " + inputPassword)
        #Already hashed in constructor
        addUser(User(inputUsername, inputEmail, inputPassword), driver)

        driver.close()
        return {"message": "Username " + inputUsername + " registered successfully"}, 201


api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(HelloWorld, '/helloworld')


if __name__ == '__main__':
    app.run(debug=True)
