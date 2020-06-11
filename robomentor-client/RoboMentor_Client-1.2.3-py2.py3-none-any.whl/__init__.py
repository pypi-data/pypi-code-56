# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import sys
import os
import socket
import re
import uuid
import time
import json
import platform
import threading
from .utils import Log
from .service import Message, Service, System
from .function import Serial
from .device import GPIO
from .__config__ import __apiUrl__, __messageUrl__, __version__

if len(sys.argv) < 3:
    Log.error("Input app_id OR app_secret Error")
    sys.exit(0)

class Init:

    def __init__(self):

        Log.info("RoboMentor_Client " + __version__)

        auth_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

        headers = {
            "Content-Type": "application/json",
            "Robot-Token": sys.argv[1] + "@" + sys.argv[2] + "@" + auth_time
        }

        params_ip = self.get_host_ip()

        params_mac = self.get_mac_address()

        params_platform = self.get_platform()

        params = {"app_id": sys.argv[1], "app_secret": sys.argv[2], "robot_mac": params_mac, "robot_ip": params_ip, "robot_platform": params_platform, "robot_version": __version__}

        res = Service.api(__apiUrl__ + "/oauth/robot/register", params, headers, 'GET')

        res_json = res.json()

        assert res_json["code"] == 0, Log.error("Robot Init Error")

        if res_json["code"] != 0:
            sys.exit(0)

        self.app_id = str(sys.argv[1])
        self.app_secret = str(sys.argv[2])
        self.ip = str(params_ip)
        self.mac = str(params_mac)
        self.token = str(res_json["data"]["token"])
        self.name = str(res_json["data"]["robot_title"])
        self.net_ip = str(res_json["data"]["robot_net_ip"])
        self.version = str(__version__)
        self.message = Message(__messageUrl__, self.mac, self.app_id, self.app_secret).start()
        self.system_task_thread = threading.Thread(target=self.system_task)
        self.system_task_thread.start()
        self.robot_task_thread = threading.Thread(target=self.robot_task)
        self.robot_task_thread.start()
        notice_data = {"message_type": "robot_run", "robot_run": {"type": "start_success"}}
        self.message.publish(json.dumps(notice_data))

    def system_task(self):
        system = System()
        while True:
         notice_data = {"message_type": "system_message", "system_message": {"time": time.strftime('%H:%M:%S', time.localtime(time.time())), "cpu": system.get_cpu_info(), "memory": system.get_memory_info()}}
         self.message.publish(json.dumps(notice_data))
         time.sleep(2)

    def robot_task(self):
        while True:
            robot_message = self.message.read_robot_message()
            if robot_message is not None:
                robot_message_json = json.loads(robot_message)
                if robot_message_json["message_type"] == "robot_config":
                    robot_config = json.loads(robot_message_json["robot_config"]["content"])
                    self.name = robot_config["robot_title"]
                if robot_message_json["message_type"] == "robot_run":
                    if robot_message_json["robot_run"]["type"] == "update":
                        os.system("sudo cp /robot/RoboMentor_Client/robot.py /robot/RoboMentor_Client/robot.bak")
                        robot_file = open("/robot/RoboMentor_Client/robot.py", 'w')
                        robot_file.write(robot_message_json["robot_run"]["content"])
                        robot_file.close()
                        notice_data = {"message_type":"robot_run","robot_run":{"type":"update_success"}}
                        self.message.publish(json.dumps(notice_data))
                    if robot_message_json["robot_run"]["type"] == "restart":
                        robot_restart = os.popen("sudo sh /robot/RoboMentor_Client/robot_restart.sh " + self.app_id + " " + self.app_secret).read()
                        if robot_restart != "success":
                            notice_data = {"message_type": "robot_run", "robot_run": {"type": "start_error"}}
                            self.message.publish(json.dumps(notice_data))
                if robot_message_json["message_type"] == "serial_message":
                    serial_conn = Serial(robot_message_json["serial_message"]["port"], robot_message_json["serial_message"]["rate"], robot_message_json["serial_message"]["size"])
                    serial_conn.write(robot_message_json["serial_message"]["content"])
                    if robot_message_json["serial_message"]["switch"] :
                        serial_data = serial_conn.read()
                        notice_data = {"message_type": "serial_message_read", "serial_message_read": {"content": serial_data}}
                        self.message.publish(json.dumps(notice_data))


    @staticmethod
    def get_host_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip_adds = s.getsockname()[0]
        finally:
            s.close()
        return ip_adds

    @staticmethod
    def get_mac_address():
        return ":".join(re.findall(r".{2}", uuid.uuid1().hex[-12:]))

    @staticmethod
    def get_platform():
        return platform.system() + " " + platform.machine()