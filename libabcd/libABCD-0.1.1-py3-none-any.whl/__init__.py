# generic use functions
from .init import init,init_without_connect
from .handling import add_handler
from .parse import parsemsg
from .network import connect,close,handle,addmessage
from .logging import die
from .watchdog import check,start
#internal functions
from .logging import _init_log_settings

###
# Logging in UTC
###
import logging
import time
logging.Formatter.converter = time.gmtime

# libABCD internal variables
name=__name__
logger=logging.getLogger(__name__)  # by default log as libABCD
cmd_switch={}

import selectors
network_info={}
network_info["host"]='localhost'
network_info["port"]=9818
network_info["selector"]=selectors.DefaultSelector()
network_info["isconnected"]=False
network_info["name"]='Unknown'
network_info["outgoing"]=[]
network_info["last_ping"]=time.time()



###
# logger init code
###
_init_log_settings(logger)

