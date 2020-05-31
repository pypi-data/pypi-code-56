# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import paho.mqtt.client as mqtt
from ..utils import Log
from ..robot import Robot


class Message:

    def __init__(self, host, client_id, username, password):
        self.host = host
        self.port = 1883
        self.client_id = client_id
        self.username = username
        self.password = password
        self.mqtt_client = None
        self.timeout = 60
        self.message = ""

    def on_connect(self, client, userdata, flags, rc):
        self.mqtt_client.message_callback_add("robot-" + self.client_id, Robot.message)
        self.subscribe("robot/" + self.client_id)

    def on_message(self, client, userdata, msg):
        self.message = str(msg.payload)
        Log.debug("收到远程消息：" + str(msg.payload))

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic, 0)

    def publish(self, topic, blob):
        self.mqtt_client.publish(topic, blob)

    def start(self):
        if self.mqtt_client is None:
            self.mqtt_client = mqtt.Client("robot-" + self.client_id)
            self.mqtt_client.username_pw_set(self.username, self.password)
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.connect(self.host, self.port, self.timeout)
            self.mqtt_client.loop_start()

    def stop(self):
        if self.mqtt_client is not None:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self.mqtt_client = None
