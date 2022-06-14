from os import getenv
from string import Template
from pathlib import Path

from py2neo import Graph


class DB:
    graph: Graph
    
    def __init__(self):
        self.requests_path = Path(__file__).parent / "requests"
        
        envs = ["DB_URL", "DB_USER", "DB_PASS"]
        if None in map(getenv, envs):
            raise EnvironmentError(f"This env var must be set : {' - '.join(filter(lambda x: getenv(x) is None, envs))}")
        else:
            self.graph = Graph(getenv("DB_URL"), auth=(getenv("DB_USER"), getenv("DB_PASS")))

    def run(self, cmd: str):
        return self.graph.run(cmd).data()

    def get_ingredient_ids_from_name(self, name):
        return self.run(f"MATCH (i:Ingredient) WHERE id(i)={name} RETURN i.name AS n")[0]['n']

    def get_ingredients_ids(self) -> list:
        return [ing['id'] for ing in self.run("MATCH (i:Ingredient) RETURN id(i) AS id")]

    def get_recipe_full_match(self, excluded_ingredients: list, start, limit) -> list:
        """recipes that are possible STRICTLY with user ingredients"""
        with open(self.requests_path / "full_match.template") as f:
            return self.run(Template(f.read()).substitute(
                excluded_ingredients=str(excluded_ingredients),
                start=str(start),
                limit=str(limit)
            ))

    def get_recipe_partial_match(self, excluded_ingredients: list, start, limit) -> list:
        """search for recipes that are APPROXIMATE matches (1 single ingredient that the user doesn't have)"""
        with open(self.requests_path / "partial_match.template") as f:
            return self.run(Template(f.read()).substitute(
                excluded_ingredients=str(excluded_ingredients),
                start=str(start),
                limit=str(limit)
            ))
