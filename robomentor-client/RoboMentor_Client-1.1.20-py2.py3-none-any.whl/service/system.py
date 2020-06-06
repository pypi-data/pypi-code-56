# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import psutil

class System:

    def __init__(self):
        self.cpu_percent = 0.00
        self.memory_percent = 0.00

    def get_cpu_info(self):
        self.cpu_percent = psutil.cpu_percent(interval=1)
        return self.cpu_percent

    def get_memory_info(self):
        virtual_memory = psutil.virtual_memory()
        self.memory_percent = virtual_memory.percent
        return self.memory_percent

