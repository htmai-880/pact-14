from .db import DB


def remove():
    db = DB()
    
    nb_recipes_deleted = db.run("""MATCH (r:Recipe:CreatedByAI)
    WHERE r.ai_creation_datetime < date() - duration({days: 7})
    DETACH DELETE r
    RETURN count(r)""")

    print(f'{nb_recipes_deleted} recipes deleted by automatic cleaning.')
