import sys, os

from .log_pb2 import Log
from .property_pb2 import *

# TODO At present, command_pb2 depends on property_pb2, but python generated code use absolute import (`import xxx`)
# A workaround is add dir into sys.path
pkgdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pkgdir)
from .info_pb2 import (Info, StatusMeta)
from .command_pb2 import *

# NOTE __version__ will be generate from cmake
__version__ = "1.1.0"

__all__ = ("info_pb2", "log_pb2", "property_pb2", "command_pb2", 
        "Info", "StatusMeta",
        "Log",
        "Property", "PropertyChange", "PropertyChoice", "PropertyInt", "PropertyDouble", "PropertyString",
        "Command", "ArgDesc", "CommandDesc", "Response",
)

