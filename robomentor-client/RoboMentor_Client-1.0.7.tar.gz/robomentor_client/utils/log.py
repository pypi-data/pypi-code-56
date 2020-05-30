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
    def debug(self, content):
        logging.debug(content)

    @staticmethod
    def info(self, content):
        logging.debug(content)

    @staticmethod
    def warning(self, content):
        logging.debug(content)

    @staticmethod
    def error(self, content):
        logging.debug(content)
