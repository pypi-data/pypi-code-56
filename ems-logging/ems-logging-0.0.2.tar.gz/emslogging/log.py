import logging
import sys
import time
import os


def default_logging_config():

    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=os.environ.get("EMS_LOG_LEVEL", "INFO"),
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout
    )

    logging.Formatter.converter = time.gmtime


