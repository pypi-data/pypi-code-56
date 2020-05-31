# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import paho.mqtt.client as mqtt
from queue import Queue
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
        self.queue = Queue()

    def on_connect(self, client, userdata, flags, rc):
        Log.info("1111")
        self.mqtt_client.message_callback_add("robot/" + self.client_id, Robot.message)
        self.subscribe("robot/" + self.client_id)

    def on_message(self, client, userdata, msg):
        Log.info("2222")
        Log.info(self.client_id + "：" + str(msg.payload))
        self.queue.put(msg)

    def subscribe(self, topic):
        Log.info("3333")
        self.mqtt_client.subscribe(topic, 0)

    def publish(self, topic, blob):
        self.mqtt_client.publish(topic, blob)

    def start(self):
        Log.info("0000")
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
