"""
GMLP.NeuralNet
==============
"""
from __future__ import absolute_import


class BaseConnectionLayers:
    def __init__(self):
        self.layers = []
    
    def __call__(self):
        return self.layers


class Connection(BaseConnectionLayers):
    def __init__(self):
        super(Connection, self).__init__()
    
    def connect(self, connection1, connection2):
        self.cn1 = connection1
        self.cn2 = connection2
        return self.layers.append([self.cn1, self.cn2])

    def show(self):
        print(self.layers)
