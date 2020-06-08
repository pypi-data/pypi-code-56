import os
from ctypes import *

path = os.path.join(os.path.dirname(__file__), "lib\\snn.dll")
snn = cdll.LoadLibrary(path)
