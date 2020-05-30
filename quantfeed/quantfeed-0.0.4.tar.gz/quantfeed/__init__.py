# -*- coding: utf-8 -*-

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __copyright__, __cake__

from .api import set_default_data_host, \
    get_future_contract, get_main_contract, \
    get_future_tick, get_future_bar, get_realtime_tick, get_realtime_min

logging.getLogger(__name__).addHandler(NullHandler())
