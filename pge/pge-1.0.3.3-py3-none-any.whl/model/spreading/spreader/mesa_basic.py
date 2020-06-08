import math
from enum import Enum
import networkx as nx

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid


class InfNetwork(Model):
    def __init__(self, graph, agent, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.G = graph.get_nx_graph()
        self.grid = NetworkGrid(self.G)


class InfAgent(Agent):
    def __init__(self, id, model, message):
        super().__init__(id, model)
        self.init_messages = message
