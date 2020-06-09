"""
GMLP.settings
==============
"""
from __future__ import absolute_import

import os


class Search:
    def __init__(self, filepath):
        self.fp = filepath
        self.files = []

    def __call__(self):
        with open(os.path.basename(self.fp), 'r') as path:
            self.files.appends(path.read())
        
    def __str__(self):
        return self.files


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


class Settings:
    def __init__(self, settings: dict, in_file: False, file_dir: False):
        self.settings = settings
        self.in_file = in_file
        self.dir = file_dir
        if self.in_file == True:
            if self.dir == True:    
                self.string = Connection()
                self.string.connect('file', Search(self.dir))
        self.string.show()
        
