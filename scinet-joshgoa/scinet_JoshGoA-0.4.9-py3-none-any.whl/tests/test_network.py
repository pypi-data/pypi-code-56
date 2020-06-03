import unittest

from scinet import Graph


class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.G = Graph()

    def test_init(self):
        self.assertFalse(self.G)

    def test_add_vertex(self):
        for vertex in range(5):
            self.G.add_vertex(vertex)
            self.assertIn(vertex, self.G)

    def test_remove_vertex(self):
        self.test_add_vertex()
        for vertex in set(self.G):
            self.G.remove_vertex(vertex)
            self.assertNotIn(vertex, self.G)

    def test_add_edge(self):
        for edge, source_vertex, target_vertex in zip(range(5), range(5), range(5)):
            self.G.add_edge(edge, source_vertex=source_vertex, target_vertex=target_vertex)
            self.assertIn(edge, self.G[source_vertex][target_vertex])

    def test_remove_edge(self):
        self.test_add_edge()
        for source_vertex, neighbors in self.G.items():
            for target_vertex, edges in neighbors.items():
                edge_count = len(edges)
                for edge in edges:
                    self.G.remove_edge(edge, source_vertex=source_vertex, target_vertex=target_vertex)
                    if edge_count:
                        self.assertNotIn(target_vertex, self.G[source_vertex])
                    else:
                        self.assertNotIn(edge, self.G[source_vertex][target_vertex])


if __name__ == '__main__':
    unittest.main()
