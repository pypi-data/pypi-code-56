# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import serial
from ..utils import Log

class Serial:

    def __init__(self, port, baudrate, stopbits, timeout: float = 0.2):

        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.timeout = timeout
        self.conn = None
        self.readData = ""

    def open(self):

        status = False

        try:
            self.conn = serial.Serial(self.port, self.baudrate, self.timeout)
            if self.conn.is_open:
                status = True
        except Exception as e:
            Log.error(e)

        return self.conn, status

    def write(self, command):

        try:
            self.conn.write(command)
        except Exception as e:
            Log.error(e)

    def close(self):

        self.conn.close()

