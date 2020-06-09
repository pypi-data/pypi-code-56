import os
from ctypes import *


class Snn:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "lib\\snn.dll")
        self.snn = cdll.LoadLibrary(path)

    def add(self, a: int, b: int) -> int:
        return self.snn.add(a, b)

    def net_count(self) -> int:
        return self.snn.SnnAPI_netCount()

    def create_net(self) -> int:
        return self.snn.SnnAPI_createNet()