# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import logging

class Log:

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s][%(asctime)s][%(filename)s(line:%(lineno)d)]: %(message)s"
    )

    @staticmethod
    def debug(content):
        logging.basicConfig(format="\033[32m [%(levelname)s][%(asctime)s][%(filename)s(line:%(lineno)d)]: %(message)s \033[0m")
        logging.debug(content)

    @staticmethod
    def info(content):
        logging.basicConfig(format="\033[34m [%(levelname)s][%(asctime)s][%(filename)s(line:%(lineno)d)]: %(message)s \033[0m")
        logging.info(content)

    @staticmethod
    def warning(content):
        logging.basicConfig(format="\033[35m [%(levelname)s][%(asctime)s][%(filename)s(line:%(lineno)d)]: %(message)s \033[0m")
        logging.warning(content)

    @staticmethod
    def error(content):
        logging.basicConfig(format="\033[31m [%(levelname)s][%(asctime)s][%(filename)s(line:%(lineno)d)]: %(message)s \033[0m")
        logging.error(content)
