import logging
import libABCD

def init_without_connect(n):
    # setting system-wide name
    libABCD.name=n
    # setting logger
    libABCD.logger=logging.getLogger(libABCD.name)
    libABCD._init_log_settings(libABCD.logger)

def init(n):
    init_without_connect(n)
    libABCD.connect(n)

