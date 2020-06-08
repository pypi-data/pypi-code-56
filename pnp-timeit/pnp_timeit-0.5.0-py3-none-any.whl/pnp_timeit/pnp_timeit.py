
import os
import json
import functools
import logging
from datetime import datetime

class Pnp_Timeit:
    """
    Provide code level time cost measurement.

    Pnp_Timeit can be swtiched ON or OFF, default is OFF.
    """
    
    G_ENABLE_TIMEIT = False
    G_LOGGER_DEFAULT_NAME = "pnp.library"
    G_LOGGER = None

    @classmethod
    def timeit(cls, func):
        @functools.wraps(func)
        def wrapper_timeit_func(*args, **kwargs):
            if cls.is_enable():
                time_begin = datetime.utcnow()

                response = func(*args, **kwargs)

                time_end = datetime.utcnow()
                time_diff_seconds = (time_end - time_begin).total_seconds()
                if cls.G_LOGGER is None:
                    logger = logging.getLogger(cls.G_LOGGER_DEFAULT_NAME)
                    logger.addHandler(logging.StreamHandler())
                    logger.setLevel(logging.INFO)
                else:
                    logger = cls.G_LOGGER

                dict_time_info = {"func": func.__name__, "args":args, "kwargs":kwargs, "time_cost_seconds":time_diff_seconds}
                logger.info("{}".format(json.dumps(dict_time_info, default=cls.__default_converter)))

                return response
            else:
                return func(*args, **kwargs)
            
        return wrapper_timeit_func


    @classmethod
    def enable(cls, logger=None):
        """
        Process scope enable, default is OFF 
        """
        Pnp_Timeit.G_ENABLE_TIMEIT = True
        if logging:
            cls.G_LOGGER = logger


    @classmethod
    def disable(cls):
        """
        Session level disable, default is DISABLE
        """
        Pnp_Timeit.G_ENABLE_TIMEIT = False
        cls.G_LOGGER = None
        
    @classmethod
    def is_enable(cls) -> bool:
        """
        Check whether timeit is enabled

        Return: 
            True: enabled
            False: disabled
        """
        return Pnp_Timeit.G_ENABLE_TIMEIT


    @classmethod
    def __default_converter(cls, pi_obj):
        """
        Convert datatime type to string
        """
        if isinstance(pi_obj, datetime):
            return pi_obj.__str__()
