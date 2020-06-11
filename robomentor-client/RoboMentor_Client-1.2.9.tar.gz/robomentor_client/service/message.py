# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import json
import paho.mqtt.client as mqtt
from queue import Queue, PriorityQueue


class Message:

    def __init__(self, host, client_id, username, password):
        self.host = host
        self.port = 1883
        self.client_id = client_id
        self.username = username
        self.password = password
        self.mqtt_client = None
        self.timeout = 60
        self.remote_message = Queue(100)
        self.robot_message = PriorityQueue(100)

    def on_connect(self, client, userdata, flags, rc):
        self.subscribe("robot/" + self.client_id)

    def on_message(self, client, userdata, msg):
        message_data = json.loads(msg.payload)
        if message_data["message_type"] == "remote_message":
            self.remote_message.put(str(msg.payload, encoding="utf-8"))
        else:
            self.robot_message.put(str(msg.payload, encoding="utf-8"))

    def read_remote_message(self):
        data = None
        if not self.remote_message.empty():
            data = self.remote_message.get()
        return data

    def read_robot_message(self):
        data = None
        if not self.robot_message.empty():
            data = self.robot_message.get()
        return data

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic, 0)

    def publish(self, blob):
        self.mqtt_client.publish("robot/" + self.client_id, blob)

    def start(self):
        if self.mqtt_client is None:
            self.mqtt_client = mqtt.Client("robot-" + self.client_id)
            self.mqtt_client.username_pw_set(self.username, self.password)
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.connect(self.host, self.port, self.timeout)
            self.mqtt_client.loop_start()

        return self

    def stop(self):
        if self.mqtt_client is not None:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self.mqtt_client = None
