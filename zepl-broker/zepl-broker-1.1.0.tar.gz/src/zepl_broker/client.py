#! /usr/bin/env python3
#
# example client implementations
#
# This file is part of Zepl Broker: https://gitlab.com/zepl1/zepl-broker
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3
import json, zmq
from pprint import pprint

class ClientLog:
    def cnt_log(self):
        self.log.recv_multipart()

    def get_log(self):
        dev_id, prefix, msg = self.log.recv_multipart()
        return dev_id.decode(), prefix.decode(), msg.decode()

    def print_log(self):
        dev_id, prefix, msg = self.log.recv_multipart()
        print(f'{dev_id.decode()} -- {prefix.decode()} --  {msg.decode()}')

    def log_sub(self, dev_id):
        self.log.subscribe(dev_id.encode())

    def log_unsub(self, dev_id):
        self.log.unsubscribe(dev_id.encode())

class ClientCtrl:
    def show_devices(self):
        print_str = 'Remote Devices: '
        cmd = ['get']
        self.req_rep(self.ctrl, print_str, cmd)

    def add_device(self, dev_id, cfg):
        print_str = f'Added {dev_id}: '
        cmd = ['add', dev_id, json.dumps(cfg)]
        self.req_rep(self.ctrl, print_str, cmd)

    def rem_device(self, dev_id):
        print_str = f'Removed {dev_id}: '
        cmd = ['rem', dev_id]
        self.req_rep(self.ctrl, print_str, cmd)

class Client(ClientLog, ClientCtrl):
    def __init__(self, ctx, broker_ip):
        super().__init__()

        self.log = ctx.socket(zmq.SUB)
        self.log.connect(f'tcp://{broker_ip}:9000')
        #self.log.setsockopt(zmq.CONFLATE, True)

        self.dev = ctx.socket(zmq.DEALER)
        self.dev.connect(f'tcp://{broker_ip}:9001')

        self.ctrl = ctx.socket(zmq.DEALER)
        self.ctrl.connect(f'tcp://{broker_ip}:9002')

    def req_rep(self, sock, print_str, cmd):
        cmd = [s.encode() for s in cmd]
        sock.send_multipart(cmd)
        try:
            resp = sock.recv_multipart()
            print(f'{print_str}: ', resp)
        except Exception as e:
            print('req_rep exception: ', e)

class DummyDevice:
    def greet(self, dev_id):
        print_str = f'greeting {dev_id} runner -- '
        cmd = [dev_id, 'runner', 'greetings']
        self.req_rep(self.dev, print_str, cmd)

        print_str = f'greeting {dev_id} device -- '
        cmd = [dev_id, 'device', 'greetings']
        self.req_rep(self.dev, print_str, cmd)

    def start_task(self, dev_id, target, task_name, task_id, arg={}):
        print_str = f'starting {dev_id}:{target}:{task_name} -- '
        cmd = [dev_id, target, 'start', task_name, task_id, json.dumps(arg)]
        self.req_rep(self.dev, print_str, cmd)

    def stop_task(self, dev_id, target, task_name):
        print_str = f'stopping {dev_id}:{target}:{task_name} -- '
        cmd = [dev_id, target, 'stop', task_name]
        self.req_rep(self.dev, print_str, cmd)

class WebReplDevice:
    def greet(self, dev_id):
        print_str = f'greeting {dev_id} -- '
        cmd = [dev_id, 'runner', 'greetings']
        self.req_rep(self.dev, print_str, cmd)

    def run_app(self, dev_id, app_char):
        print_str = f'running app {app_char} on {dev_id} -- '
        cmd = [dev_id, 'runner', 'run', app_char]
        self.req_rep(self.dev, print_str, cmd)

    def sync_files(self, dev_id):
        print_str = f'syncing files {dev_id} -- '
        cmd = [dev_id, 'runner', 'sync']
        self.req_rep(self.dev, print_str, cmd)

    def send(self, dev_id, msg):
        print_str = f'sending {msg} to {dev_id} -- '
        cmd = [dev_id, 'runner', 'send', msg]
        self.req_rep(self.dev, print_str, cmd)

class WebReplFiles:
    pass

class WebReplClient(Client, WebReplDevice):
    def __init__(self, ctx, broker_ip):
        super().__init__(ctx, broker_ip)

class DummyClient(Client, DummyDevice):
    def __init__(self, ctx, broker_ip):
        super().__init__(ctx, broker_ip)
