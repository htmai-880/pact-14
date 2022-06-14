from py2neo import Graph
import matplotlib.pyplot as plt
import numpy as np

graph = Graph("bolt://localhost:7687", auth=('neo4j', 'pact2020'))

data = graph.run(
    "MATCH (:Recipe)-[h:HAS_INGREDIENT]->(i:Ingredient) RETURN i.name AS n, count(h) AS c ORDER BY c DESC").data()

freqs = []
s = 0
for i in data:
    s += i['c']
    freqs.append(i['c'])

N = len(freqs)
RANGE = np.array(list(range(1, N + 1)))

plt.plot(RANGE, np.array(freqs) / s)

plt.xlabel('rang')
plt.ylabel('nb_usage')
plt.yscale('log')
plt.xscale('log')
plt.grid(True)

# zipf distribution
optimal_zipf = 1 / (RANGE * np.log(1.78 * N))
plt.plot(RANGE, optimal_zipf)

plt.show()
