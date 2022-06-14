"""
Test the ia module api.
"""
import pytest
from app.common.ingredient import Ingredient
from app.common.errors import IngredientError

t1 = {"id": 1, "amount": 1, "unit": "L"}
t2 = {"id": 2, "amount": 2, "unit": "L"}
t3 = {"id": 3, "amount": 3, "unit": "L"}


tests = [
    (t1, t1, '{"id": 1, "amount": 1, "unit": "L"}'),
    (t2, t2, '{"id": 2, "amount": 2, "unit": "L"}'),
    (t3, t3, '{"id": 3, "amount": 3, "unit": "L"}')
]

wrong_tests = [
    ({"id": 1}),
    ({"amount": 1}),
    (dict()),
    ({"id": 1, "amount": 1, "another": 5}),
    ({"id": 1, "amount": "text"}),
    ({"id": 5, "amount": 1})
]


@pytest.mark.parametrize("dico, i_data, str_i", tests)
def test_good_params(dico, i_data, str_i):
    i = Ingredient(**dico)
    assert i.data == i_data
    assert i.json == i_data
    assert str(i) == str_i


@pytest.mark.parametrize("wrong", wrong_tests)
def test_wrong_params(wrong):
    with pytest.raises(IngredientError):
        Ingredient(**wrong)
