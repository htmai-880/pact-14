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
            raise EnvironmentError(
                f"This env var must be set : {' - '.join(filter(lambda x: getenv(x) is None, envs))}")
        else:
            self.graph = Graph(getenv("DB_URL"), auth=(getenv("DB_USER"), getenv("DB_PASS")))

    def run(self, cmd: str):
        return self.graph.run(cmd).data()

    def get_ingredient_name_from_id(self, ing_id):
        return self.run(f"MATCH (i:Ingredient) WHERE id(i)={ing_id} RETURN i.name AS n")[0]['n']

    def get_user_ingredients_ids(self, user_email):
        with open(self.requests_path / "user_ingredients_ids.template") as f:
            return self.run(Template(f.read()).substitute(
                user_email=str(user_email)
            ))[0]['ings_ids']

    def get_recipe_full_match(self, user_email: str, start, limit) -> list:
        """recipes that are possible STRICTLY with user ingredients"""
        with open(self.requests_path / "full_match.template") as f:
            return self.run(Template(f.read()).substitute(
                user_email=str(user_email),
                start=str(start),
                limit=str(limit)
            ))

    def get_recipe_partial_match(self, user_email: str, start, limit) -> list:
        """search for recipes that are APPROXIMATE matches (1 single ingredient that the user doesn't have)"""
        with open(self.requests_path / "partial_match.template") as f:
            possible_recipes = self.run(Template(f.read()).substitute(
                user_email=str(user_email),
                start=str(start),
                limit=str(limit)
            ))

            return possible_recipes

    def clone_recipes(self, recipe_id, ing_to_replace, substitute) -> list:
        """clone and return recipes"""
        # todo : faire pour plusieurs recipes a la fois
        # clone recipes with label "CreatedByAI"
        with open(self.requests_path / "clone_recipes.template") as ff:
            try:
                cloned_recipe = self.run(Template(ff.read()).substitute(
                    recipe_id=str(recipe_id),
                    ing_to_replace=str(ing_to_replace),
                    substitute=str(substitute)
                ))
                clone_id = cloned_recipe[0]['id']
                clone_title = cloned_recipe[0]['title']
                with open(self.requests_path / "clone_recipes2.template") as fff:
                    self.run(Template(fff.read()).substitute(
                        recipe_id=str(recipe_id),
                        clone_id=str(clone_id),
                        ing_to_replace=str(ing_to_replace)
                    ))
                return [{'id': clone_id, 'title': clone_title}]
            except IndexError:
                return []
