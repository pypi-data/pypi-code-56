# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

from ..utils import Log


class Robot(object):

    @staticmethod
    def start():
        pass

    @staticmethod
    def close():
        pass

    @staticmethod
    def message(client, userdata, message):
        Log.info("我是类，收到远程消息：" + str(message))
