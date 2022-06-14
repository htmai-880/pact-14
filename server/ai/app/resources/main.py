"""
Recipe API : recipes from ingredients
"""
from flask_restful import Resource, marshal_with

from ..common.input_parser import get_args
from ..common.output_fields import ai_response
from ..ai import get_recipe


# noinspection PyMethodMayBeStatic
class Main(Resource):
    """
    Main api class
    """

    # pylint: disable=R0201
    @marshal_with(ai_response)
    def get(self):
        """ Respond to GET protocol.
        """
        return {"recipes_id": get_recipe(get_args())}

    # pylint: disable=R0201
    @marshal_with(ai_response)
    def post(self):
        """ Respond to POST protocol.
        """
        return {"recipes_id": get_recipe(get_args())}
