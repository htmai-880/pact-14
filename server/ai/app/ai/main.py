"""
IA module entrypoint.
"""
from .db import DB
from .model import Model


def get_recipe(user_email: str, limit=20, startsfrom=0) -> list:
    """ Get recipe from api call.

    Parameters
    ----------
    user_email: str
        user email
    limit: int
        how many recipes to return
    startsfrom: int
        first ingredient to return

    Returns
    -------
    list(int)
        all matching recipes ids
        index 0 is the better
    """

    db = DB()

    possible_recipes = db.get_recipe_full_match(user_email, startsfrom, limit)
    possible_recipes = [{'id': x['id'], 'title': x['title']} for x in possible_recipes]

    if len(possible_recipes) >= limit:
        return possible_recipes
    else:
        # todo : stops only when limit is found
        partial_match_recipes = db.get_recipe_partial_match(user_email, start=0, limit=100)

        mod = Model()

        similarities = []
        clones_ids = []
        for recipe in partial_match_recipes:
            # find missing ingredients
            user_ingredients_ids = db.get_user_ingredients_ids(user_email)
            missing_ing = list(set(recipe['ingredients_ids']).difference(user_ingredients_ids))[0]
            name = db.get_ingredient_name_from_id(missing_ing)

            # find similar ingredients
            similar_ing_token, sim = mod.most_similar(name)

            if sim is not None:
                # similar ingredient token in ingredient2vec model => name in database
                substitute = mod.get_name_from_token(similar_ing_token)

                # keep all similarities
                similarities.append(sim)

                # clone recipe
                # todo : clone recipes as a whole
                clone = db.clone_recipes(recipe['id'], name, substitute)
                clones_ids.extend(clone)

        print(clones_ids)
        # return ids from possible_recipes ranked by missing_ing substitutable-ness
        # return possible_recipes + [x for _, x in sorted(zip(similarities, clones_ids))]
        # todo : bug with sorted
        all_recipes = possible_recipes + clones_ids
        return [x['id'] for x in all_recipes]
