# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

from abc import ABCMeta, abstractmethod
from ..utils import Log


class Robot(metaclass=ABCMeta):

    @abstractmethod
    def onstart(self):
        pass

    @abstractmethod
    def onclose(self):
        pass

    @abstractmethod
    def onmessage(self, message):
        Log.info("收到远程消息：" + str(message))
