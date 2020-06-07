import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from .ads1115 import *
from xpi_blocks.smbus_m import *
#from DS1302 import *
#from ds1307 import *
