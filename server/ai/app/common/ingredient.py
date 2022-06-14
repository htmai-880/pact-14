"""
Define an ingredient
"""
from .errors import IngredientError
from .rest_resource import RestResource


# pylint: disable=R0903
class Ingredient(RestResource):
    """
    An ingredient as two fields : type and amount.
    """
    exception = IngredientError
    inner_dict = {"id": int, "amount": int, "unit": str}
