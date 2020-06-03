import unittest

from scinet import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.G = Graph()

    def test_init(self):
        self.assertFalse(self.G)

    def test_add_vertex(self):
        for vertex in range(5):
            self.G.add_vertex(vertex)
            self.assertIn(vertex, self.G)

    def test_add_edge(self):
        for source_vertex, target_vertex, edge in zip(range(5), range(5), range(5)):
            self.G.add_edge(source_vertex, target_vertex, edge)
            self.assertIn(edge, self.G[source_vertex][target_vertex])

    def test_remove_vertex(self):
        self.test_add_vertex()
        for vertex in set(self.G.vertices()):
            self.G.remove_vertex(vertex)
            self.assertNotIn(vertex, self.G)

    def test_remove_edge(self):
        self.test_add_edge()
        for source_vertex, target_vertex in set(self.G.edges()):
            self.G.remove_edge(source_vertex, target_vertex)
            self.assertNotIn(target_vertex, self.G[source_vertex])


if __name__ == '__main__':
    unittest.main()
