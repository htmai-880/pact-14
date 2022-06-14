"""
Parse request to get a simple dict instead of a string.
"""
from json import loads

from flask_restful.reqparse import RequestParser

from .ingredient import Ingredient

ia_parser = RequestParser(bundle_errors=True)
ia_parser.add_argument("user_email", required=True)


def get_args():
    """
    parse request args and return ingredients
    :return: list[Ingredient]
    """
    args = ia_parser.parse_args()
    return args["user_email"]
