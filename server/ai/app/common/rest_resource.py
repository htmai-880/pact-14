"""
A basic resource abstract
"""
from json import dumps

from .errors import ResourceError


# noinspection PyCallingNonCallable
class RestResource:
    """
    A resource is a simple dict that can be json serialized.

    Parameters
    ----------
    exception: Exception
        exception to raise if errors
    inner_dict: dict
        data types dict
        { "name 1" : str, "name 2" : int ...}
    """
    exception: ResourceError
    inner_dict: dict

    def __init__(self, **kwargs):
        """ init resource
        """
        try:
            for e_name, e_type in self.inner_dict.items():
                e_data = kwargs[e_name]
                if e_name in kwargs.keys():
                    if isinstance(e_data, e_type):
                        setattr(self, e_name, e_data)
                    else:
                        raise AttributeError(f"Argument {e_name} must be of type {e_type}, get {type(e_data)}.")
                else:
                    raise AttributeError(f"Argument {e_name} needed.")
            for k in kwargs.keys():
                if k not in self.inner_dict.keys():
                    raise AttributeError(f"Argument {k} provided but not needed.")
        except Exception as exception:
            raise self.exception() from exception

    @property
    def data(self) -> dict:
        """ object data

        Returns
        -------
        dict: all data
        """
        try:
            return {e_name: getattr(self, e_name) for e_name in self.inner_dict.keys()}
        except Exception as exception:
            raise self.exception() from exception

    def __str__(self) -> str:
        """ str(self)

        Returns
        -------
        str
        """
        try:
            return dumps(self.data)
        except Exception as exception:
            raise self.exception() from exception

    json = data
