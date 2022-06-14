import time
from os import environ

from server.ai.app.ai.main import get_recipe

environ["DB_URL"] = "bolt://localhost:11003"
environ["DB_USER"] = "neo4j"
environ["DB_PASS"] = "pact2020"

scores = []

for i in range(10):
    scores = []
    t1 = time.time()
    get_recipe("test@test.com")
    scores.append(time.time() - t1)

print(sum(scores) / len(scores))
