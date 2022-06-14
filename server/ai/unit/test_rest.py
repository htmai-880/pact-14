"""
Test the rest resource
"""
import pytest
from app.common.rest_resource import RestResource
from app.common.errors import ResourceError


class Err(ResourceError):
    default_message: str = "test error"


resource_init = ({"a": int, "b": str}, Err)


tests = [
    (resource_init, {"a": 0, "b": "str"}, '{"a": 0, "b": "str"}')
]


wrong_tests = [
    (resource_init, {"a": 0}, Err),
    (resource_init, {"b": "str"}, Err),
    (resource_init, dict(), Err),
    (resource_init, {"a": 0, "b": "str", "another": 5}, Err),
    (resource_init, {"a": "str", "b": "str"}, Err),
    (resource_init, {"a": 0, "b": 0}, Err)
]


@pytest.mark.parametrize("init, data, res", tests)
def test_good_params(init, data, res):
    class Tmp(RestResource):
        inner_dict = init[0]
        exception = init[1]
    
    t = Tmp(**data)
    assert t.data == data
    assert t.json == data
    assert str(t) == res


@pytest.mark.parametrize("init, data, error", wrong_tests)
def test_wrong_params(init, data, error):
    class Tmp(RestResource):
        inner_dict = init[0]
        exception = init[1]
    
    with pytest.raises(error):
        Tmp(**data)
