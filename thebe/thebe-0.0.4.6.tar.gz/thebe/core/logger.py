import time, sys, datetime, glob, re, sys, time, os, copy, logging, threading
logging.StreamHandler(stream=None)

def getLogger(fileLoc, name):
    logger = logging.getLogger(name)

    file_handler = logging.FileHandler('%s/logs/%s'%(os.path.dirname(__file__), fileLoc), mode='w')

    formatter = logging.Formatter('%(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(streamHandler)
    logging.StreamHandler(stream=None)

    return logger

