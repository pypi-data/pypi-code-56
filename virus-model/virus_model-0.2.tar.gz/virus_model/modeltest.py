import virusmodel as v
from analytics import LinePlot
import random

graph = v.Graph()


graph.createNodes(100)

graph.createLinks()
# print(graph.nodes)
graph.addIntervention(0.0, 2, 'lockdown', 7)

graph.simulate(1, 0.7, 10)

data = graph.data

# plot.show()

# plot  = LinePlot(graph)
# plot.plot()
print(data.head())
# node = random.choice(list(graph.nodes))


# node = graph.nodes['201c64d0-5f8f-44d1-a682-4b56f91b1698']
# print(graph.nodes[node].links)