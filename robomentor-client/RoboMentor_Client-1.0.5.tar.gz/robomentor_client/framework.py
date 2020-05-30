# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import time
import uuid
import re
import socket
from .utils import Request, Log
from .__config__ import __apiUrl__, __appID__, __appSecret__


class Framework:

    def __init__(self):

        auth_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

        auth_ip = self.get_host_ip()

        auth_mac = self.get_mac_address()

        headers = {
            "Content-Type": "application/json",
            "Robot-Token": __appID__ + "@" + __appSecret__ + "@" + auth_time
        }

        params = {"app_id": __appID__, "app_secret": __appSecret__, "robot_mac": auth_mac, "robot_ip": auth_ip}

        res = Request.do(__apiUrl__, params, headers, 'GET')

        Log.debug(res.json())

    @staticmethod
    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    @staticmethod
    def get_mac_address(self):
        return "-".join(re.findall(r".{2}", uuid.uuid1().hex[-12:].upper()))




