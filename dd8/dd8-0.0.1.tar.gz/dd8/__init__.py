# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:15:06 2019

@author: yq
"""

import logging
import os
import pathlib
import datetime
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

IS_PRODUCTION = False
if IS_PRODUCTION:
    LOG_PRINT_LEVEL = logging.WARNING
    LOG_WRITE_LEVEL = logging.ERROR
else:
    LOG_PRINT_LEVEL = logging.DEBUG
    LOG_WRITE_LEVEL = logging.WARNING

JOB_START_METHOD = 'forkserver'

NAME = __name__

TODAY = datetime.datetime.now()

def get_basic_logger(str_name,
                enum_print_level,                
                enum_file_level = None,
                str_log_file_path = None,                
                str_print_format = r'%(asctime)s:%(name)s:%(module)s:%(levelname)s:%(message)s',
                str_file_format = r'%(asctime)s:%(name)s:%(module)s:%(levelname)s:%(message)s'):
    """
    Return a logger object with an option to create a separate log file.
    
    Parameters
    ----------
    str_name : string
        name of the logger object
    enum_print_level : integer
        enum of logging level to print/display
            logging.DEBUG:      10 [detailed information, typically of interest only when dignosing problems]
            logging.INFO:       20 [confirmation that things are working as expected]
            logging.WARNING:    30 [an indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low')]
            logging.ERROR:      40 [due to a more serious problem, the software has not been able to perform some functions]
            logging.CRITICAL:   50 [a serious error, indicating that the program itself may be unable to continue running]
    str_print_format : string, optional
        string representing the format to display when printing log message,
        more formats can be found in python logging documentation,
        by default '%(asctime)s:%(name)s:%(module)s:%(levelname)s:%(message)s'
    enum_file_level : integer, optional
        enum of logging level to output into log file to allow for additional 
        flexibility where level differs from `enum_print_level` - no log file 
        will be generated if no value is given to this parameter, 
        by default None
    str_log_file_path : string
        full file path to save log file, 
        by default None
    str_file_format : string
        string representing the format to display when outputting log message,
        more formats can be found in python logging documentation,
        by default '%(asctime)s:%(name)s:%(module)s:%(levelname)s:%(message)s'
    
    Returns
    -------
    logging.RootLogger
        logger object to log messages of different levels and replace the print
        statement
            logger.debug()
            logger.info()
            logger.warning()
            logger.error()
            logger.critical()
    """
    
    logger = logging.getLogger(str_name)
    if logger.handlers:
        logger.handlers = []
    if enum_file_level:
        if not str_log_file_path:
            str_log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log/')
        if not pathlib.Path(str_log_file_path).is_dir():
            os.mkdir(str_log_file_path)
        file_handler = logging.FileHandler(str_log_file_path + str_name + '.log')
        formatter = logging.Formatter(str_file_format)
        file_handler.setLevel(enum_file_level)
        file_handler.setFormatter(formatter)        
        logger.addHandler(file_handler)
    
    logger.setLevel(enum_print_level)
    formatter = logging.Formatter(str_print_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger

