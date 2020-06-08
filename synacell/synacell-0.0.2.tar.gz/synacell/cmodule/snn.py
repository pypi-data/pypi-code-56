import os
from ctypes import *


class SNN:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "lib\\snn.dll")
        self.snn = cdll.LoadLibrary(path)

    def add(self, a: int, b: int) -> int:
        return self.snn.add(a, b)

