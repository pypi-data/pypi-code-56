#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for artellapipe-dccs-maya
"""

import os
import logging.config

# =================================================================================

PACKAGE = 'artellapipe.dccs.maya'

# =================================================================================


def init(dev=False):
    """
    Initializes module
    """

    from tpDcc.libs.python import importer
    from artellapipe.dccs.maya import register

    logger = create_logger(dev=dev)
    register.register_class('logger', logger)

    importer.init_importer(package=PACKAGE)


def create_logger(dev=False):
    """
    Returns logger of current module
    """

    logger_directory = os.path.normpath(os.path.join(os.path.expanduser('~'), 'artellapipe', 'logs'))
    if not os.path.isdir(logger_directory):
        os.makedirs(logger_directory)

    logging_config = os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))

    logging.config.fileConfig(logging_config, disable_existing_loggers=False)
    logger = logging.getLogger(PACKAGE.replace('.', '-'))
    if dev:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    return logger
