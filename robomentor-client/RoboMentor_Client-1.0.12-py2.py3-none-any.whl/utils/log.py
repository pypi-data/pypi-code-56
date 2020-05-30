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
        format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    )

    @staticmethod
    def debug(content):
        logging.debug(content)

    @staticmethod
    def info(content):
        logging.debug(content)

    @staticmethod
    def warning(content):
        logging.debug(content)

    @staticmethod
    def error(content):
        logging.debug(content)
