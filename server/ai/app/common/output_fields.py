"""
All fields to convert objects to json.
"""
from flask_restful.fields import Integer, List


ai_response = {"recipes_id": List(Integer)}
