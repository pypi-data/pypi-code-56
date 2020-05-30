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
import multiprocessing as mp
from .utils import Request, Log
from .__config__ import __apiUrl__, __messageService__

CTX = mp.get_context('spawn')


class Framework:

    def __init__(self, app_id, app_secret):
        assert app_id != "" or app_secret != "", "app_id OR app_secret Error"

        self._mu: mp.Lock = CTX.Lock()
        with self._mu:
            auth_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
            self.auth_ip = self.get_host_ip()
            self.auth_mac = self.get_mac_address()
            self.app_id = app_id
            self.app_secret = app_secret
            headers = {
                "Content-Type": "application/json",
                "Robot-Token": app_id + "@" + app_secret + "@" + auth_time
            }
            params = {"app_id": app_id, "app_secret": app_secret, "robot_mac": self.auth_mac, "robot_ip": self.auth_ip}
            res = Request.do(__apiUrl__ + "/oauth/robot/register", params, headers, 'GET')

            res_json = res.json()

            assert res_json["code"] == 0, "robot register Error"

    @staticmethod
    def get_host_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    @staticmethod
    def get_mac_address():
        return ":".join(re.findall(r".{2}", uuid.uuid1().hex[-12:]))




