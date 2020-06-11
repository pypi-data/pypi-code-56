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
        logging.debug(content)

    @staticmethod
    def info(content):
        logging.info(content)

    @staticmethod
    def warning(content):
        logging.warning(content)

    @staticmethod
    def error(content):
        logging.error(content)
