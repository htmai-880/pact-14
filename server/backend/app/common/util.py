import binascii
import os
from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()


# ******************   USER FUNCTIONS ****************** #

def generate_password_hash(password):
    return ph.hash(password)


def check_password_hash(hashed_password, input_password):
    try:
        return ph.verify(hashed_password, input_password)
    except exceptions.VerifyMismatchError:
        return False


# ****************** NEO4J FUNCTIONS ****************** #

def create_user(tx, username, email, password):
    tx.run(
        '''
        CREATE (user:User {username: $username, email: $email,
                           password: $password,
                           api_key: $api_key})
        RETURN user
        ''',
        username=username,
        email=email,
        password=password,
        api_key=binascii.hexlify(os.urandom(20)).decode()
    )


def get_user_by_username(tx, username):
    return tx.run(
        """
        MATCH (user:User {username: $username}) RETURN user
        """,
        {"username": username},
    ).single()


def get_user_by_email(tx, email):
    return tx.run(
        """
        MATCH (user:User {email: $email}) RETURN user
        """,
        {"email": email},
    ).single()


def get_users_by_username(tx, username):
    users = []
    result = tx.run(
        """
        MATCH (user:User) WHERE user.username CONTAINS $username
        RETURN user
        """,
        {"username": username},
    )
    for record in result:
        users.append(record)
    return users


# -------------------------- Recipe related functions -----------------------------------------------


def add_ingredient(tx, name):
    # todo : test
    return tx.run('''MERGE (i:Ingredient {name:toLower($name)}) RETURN id(i) AS id''', {'name': name})


def get_ingredients(tx, name):
    ingredients = []
    result = tx.run('''MATCH (i:Ingredient) WHERE i.name CONTAINS $name
                        RETURN i as i, id(i) as id''', {"name": name})
# def get_ingredient(tx, name, user_email):
#     # todo : test
#     result = tx.run(''' MATCH (i:Ingredient)
#                         WHERE i.name CONTAINS $name
#                         OPTIONAL MATCH (:User{email: $email})-[fv:FAVORITE_INGREDIENT]->(i)
#                         RETURN i as i, id(i) as id
#                         ORDER BY fv.frequency DESC''', {"name": name, "email": user_email})
    for ingredient in result:
        ingredients.append(ingredient)
    return ingredients

def get_ingredient(tx, name):
    result = tx.run('''MATCH (i:Ingredient) WHERE toLower(i.name)=toLower($name)
                        RETURN i as i, id(i) as id''', {"name": name}).single().data()
# def get_ingredient(tx, name, user_email):
#     # todo : test
#     result = tx.run(''' MATCH (i:Ingredient)
#                         WHERE i.name CONTAINS $name
#                         OPTIONAL MATCH (:User{email: $email})-[fv:FAVORITE_INGREDIENT]->(i)
#                         RETURN i as i, id(i) as id
#                         ORDER BY fv.frequency DESC''', {"name": name, "email": user_email})
    return result


def add_recipe(tx, recipe):
    tx.run(
        '''
        MATCH(u:User{email: $email})
        CREATE (r:Recipe {title: $title, instructions: $instructions, provenance:$provenance})
        CREATE (u)-[:CREATED]->(r)
        ''',
        {"title": recipe["title"], "instructions": recipe["instructions"], "email": recipe["email"], "provenance":recipe["provenance"]}
    )
    for ing in recipe["ingredients"]:
        print(ing)
        tx.run(
            '''
            MATCH (r:Recipe {title: $title})
            MATCH (i:Ingredient {name: $name})
            CREATE (r)-[:HAS_INGREDIENT {quantity_numerator: $qtt_num, quantity_denominator: $qtt_den, preparation: $prep, unit: $unit}]->(i)
            ''',
            {"title": recipe.get("title"),
             "name": ing["name"],
             "qtt_num": (ing["properties"].get("quantity_numerator") or None),
             "qtt_den": (ing["properties"].get("quantity_denominator") or None),
             "prep": (ing["properties"].get("prep") or None),
             "unit": (ing["properties"].get("unit") or None),
             }
        )


def get_recipe(tx, title):
    # TODO : remove WHERE NOT r:CreatedByAI when recipes created by ai title changed @Nicolas
    recipes = []
    result = tx.run('''MATCH (r:Recipe) WHERE NOT r:CreatedByAI AND r.title CONTAINS $title RETURN r, id(r) as idn''',
                    {'title': title})
    for recipe in result:
        recipes.append(recipe)
    return recipes  # List of recipes


def get_recipe_by_id(tx, r_id):
    # TODO : remove WHERE NOT r:CreatedByAI when recipes created by ai title changed @Nicolas
    return tx.run('''MATCH (r:Recipe) WHERE NOT r:CreatedByAI AND id(r)=$id
    RETURN r, id(r) as idn''', {'id': r_id}).single()


def get_ingredients_of_recipe(tx, title):
    """ Returns recipe AND its ingredients as well as their properties"""
    result_list = []  # ingredient class elements
    results = tx.run('''MATCH (r:Recipe {title: $title})-[rel:HAS_INGREDIENT]->(i)
    RETURN i, rel, r, id(r) as idn''', {"title": title})
    for result in results:
        result_list.append(result)
    return result_list


def get_ingredients_of_recipe_by_title(tx, r_id):
    """ Returns recipe AND its ingredients as well as their properties"""
    result_list = []  # ingredient class elements
    results = tx.run('''MATCH (r:Recipe)-[rel:HAS_INGREDIENT]->(i) WHERE id(r)=$id
                        RETURN i, rel, r, id(r) as idn''', {"id": r_id})
    for result in results:
        result_list.append(result)
    return result_list


def get_user_ingredient(tx, username):
    ingredients = []
    result = tx.run(
        """
        MATCH (user:User)-[rel:OWNS_INGREDIENT]->(i:Ingredient) WHERE user.username=$username
        RETURN i, id(rel) as own_id, rel.unit as unit, rel.quantity_numerator as quantity_numerator, rel.quantity_denominator as quantity_denominator, labels(i) as L, id(i) as idn
        """,
        {"username": username}
    )
    for record in result:
        ingredients.append(record)
    return ingredients


def get_user_recipes(tx, username):
    recipes = []
    result = tx.run(
        """
        MATCH (user:User)-[rel:CREATED]->(recipe:Recipe) WHERE user.username=$username
         RETURN recipe, id(recipe) as idn""", {"username": username}
    )
    for record in result:
        recipes.append(record)
    return recipes


def get_all_ingredients_with_units(tx):
    """get all possibles ingredients with all possibles units"""
    print("UTILISATION NON RECOMMANDEE, USE @getUnitsForIngredient INSTEAD")
    return tx.run("""
        MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
        UNWIND h AS r
        RETURN COLLECT(distinct r.unit) AS units, id(i) AS id, i.name AS name
        """).data()


def get_units_for_ingredient(tx, i_id):
    """get all possibles units for an ingredient, by id"""
    results = tx.run(f"""
        MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
        WHERE id(i)=$id
        RETURN DISTINCT h.unit AS units
        """, {"id": i_id}).data()
    return results


def get_units_for_ingredient_by_name(tx, name):
    """get all possibles units for an ingredient, by name"""
    results = tx.run(f"""
        MATCH (i:Ingredient)<-[h:HAS_INGREDIENT]-(:Recipe)
        WHERE i.name=$name
        RETURN DISTINCT h.unit AS units
        """, {"name": name}).data()
    return results


def add_ingredient_for_user(tx, ingredient_id, amount, unit, user_email, expiration_date):
    """add ingredient to  the user"""
    tx.run("""
        MATCH (u:User {email: $user_email})
        MATCH (i:Ingredient) WHERE id(i)=$ingredient_id
        CREATE (u)-[:OWNS_INGREDIENT {expiration_date: date($expiration_date), quantity_denominator:1,
        quantity_numerator:$amount, unit:$unit}]->(i)
        """, {"user_email": user_email, "ingredient_id": ingredient_id, "amount": amount, "unit": unit, "expiration_date": expiration_date})


def delete_ingredient_for_user(tx, own_id, user_email):
    """delete ingredient owned by user"""
    tx.run("""
        MATCH (User {email:$user_email})-[rel:OWNS_INGREDIENT]->(Ingredient) WHERE id(rel)=$own_id
        DELETE(rel)
        """,{
            'own_id': own_id,
            'user_email': user_email
        })


def get_all_ingredients(tx):
    """returns all ingredients"""
    return tx.run("""
            MATCH (i:Ingredient)
            RETURN i.name AS name, id(i) AS id
            """)


def find_recipe_by_id(tx, r_id):
    """return recipe infos by id"""
    # todo : to test
    print("WARNING : UNTESTED")
    recipe = tx.run(f"""
    MATCH (r:Recipe) WHERE id(r)={r_id}
    WITH r
    MATCH (r)-[:HAS_INGREDIENT]->(i:Ingredient)
    WITH r, collect(i.name) AS ingredients
    RETURN r.title AS title, r.instructions AS instructions, ingredients, labels(r) AS labels""")
    recipe['created_by_ai'] = 'CreatedByAI' in recipe['labels']
    return recipe

def get_recipe_ratings(tx, idn):
    """get recipe ratings (grade and comment)"""
    ratings = tx.run("""
    MATCH (u:User)-[rel:RATING]->(r:Recipe) WHERE id(r)=$id
    RETURN r.title as title, u.username as username, rel.grade as grade, rel.comment as comment, rel.date as date
    ORDER BY date DESC
    """,
    {'id': idn}
    ).data()
    for rating in ratings:
        rating["date"]=rating["date"].iso_format()
    return ratings

def post_recipe_rating(tx, idn, email, grade, comment):
    """post recipe rating (grade and comment)"""
    tx.run("""
    MATCH (u:User {email: $email})
    MATCH (r:Recipe) WHERE id(r)=$id
    MERGE (u)-[rel:RATING {grade: $grade, comment: $comment, date:date()}]->(r)
    """,
    {'id': idn, 'email': email, 'grade': grade, 'comment': comment})

def get_user_favorite_recipes_id(tx, email):
    return tx.run("""
    MATCH (u:User {email: $email})-[rel: LIKES_RECIPE]->(r:Recipe)
    RETURN r.title as title, id(r) as id
    """,
    {"email": email}
    ).data()

def set_user_favorite_recipe(tx, idn, email):
    tx.run("""
    MATCH (u:User {email: $email})
    MATCH (r:Recipe) WHERE id(r)=$id
    MERGE(u)-[:LIKES_RECIPE]->(r)
    """,
    {"id": idn, "email": email})

def remove_user_favorite_recipe(tx, idn, email):
    tx.run("""
    MATCH (u:User {email: $email})-[rel:LIKES_RECIPE]->(r:Recipe) WHERE id(r)=$id
    DELETE rel
    """,
    {"id": idn, "email": email})

def is_in_favorites(tx, idn, email):
    return tx.run("""
    MATCH (u:User {email: $email})-[rel: LIKES_RECIPE]->(r:Recipe) WHERE id(r)=$id
    RETURN count(*) as c
    """,
    {"id": idn, "email": email}).data()[0].get("c")