"""
Some errors defined here.
"""


class ResourceError(Exception):
    """Exception raised for errors in RestResource class.
    """
    default_message: str = "An error occurred in this resource !"

    def __init__(self, message: str = None):
        """ init error

        Parameters
        ----------
        message: str
            additional message.
        """
        self.message = message or self.default_message
        super().__init__(self.message)


class IngredientError(ResourceError):
    """Exception raised for errors in Ingredient class.
    """
    default_message: str = "An error occurred in this ingredient !"
