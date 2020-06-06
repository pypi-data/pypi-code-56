from src.reading.interaction.Interaction import Interaction
from src.reading.story.Story import Story
import networkx as nx


class SimpleGraphStory(Story):
    """The reader moves between situations by selecting from enumerated
    options. Each node stores a displayable, and a prompt uniquely
    determined by the edges going away from the node. This Story stores
    no dynamic data."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph
        self.current_node = graph["beginning"]  # Start here by convention

    def turn_page(self, interaction_result) -> Interaction:
        """The result of the previous interaction always identifies an edge to
        traverse. The next interaction is created from the text associated with
        a node and the prompt is generated from its traversable edges."""

        self.current_node = self.graph[self.current_node]
