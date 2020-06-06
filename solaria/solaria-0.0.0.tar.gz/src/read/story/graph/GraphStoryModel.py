import networkx as nx


class GraphStoryModel(object):
    """Represents a Story as a graph with nodes, organized into layers,
    and edges which connect the nodes.
    - The nodes are called Paragraphs, which contain story content that
      displays depending on the state of the Reader.
    - The edges are called Phrases, which connect Paragraphs to one
      another as well as to themselves, which change the
      state of the Reader.
    - The graph also has "layers", which are (roughly) causally-
      independent sets of nodes that overlap one another. Layers are
      defined by a field in the Paragraph class, and are used to access
      a paragraph from a particular layer in this class.
    """

    def __init__(self):
        """Default constructor. Creates a null Graph."""
        self.graph = nx.MultiDiGraph()

    # TODO "a story must be able to access its own components"
