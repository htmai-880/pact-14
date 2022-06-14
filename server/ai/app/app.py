"""
Main server runner
"""
from flask import Flask
from flask_restful import Api

from .resources import Main


app = Flask(__name__)
api = Api(app)

api.add_resource(Main, '/')


def main():
    """
    run the server
    """
    app.run(host="0.0.0.0", port=80)
