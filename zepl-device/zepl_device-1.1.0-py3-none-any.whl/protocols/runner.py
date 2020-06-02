#!/usr/bin/env python
#
# This file is part of zepl-device: https://gitlab.com/zepl1/zepl-device
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3.0-or-later

import codecs
import struct
import os
import sys

import zmq
import zmq.asyncio
import asyncio
import websockets

from time import sleep

from zmq.utils.monitor import parse_monitor_message
from pprint import pprint

class DummyRunner:
    """Passthrough runner for zmq.PAIR via tcp between DummyDevice <-> DummyIo
    """
    def __init__(self, ctx, uri_dev_io, cfg, loop=None):
        #self.loop = loop if loop else asyncio.new_event_loop()
        self.z_sock = ctx.socket(zmq.PAIR)
        self.z_sock.bind(uri_dev_io)

        dummy_uri = f'tcp://{cfg["dev_ip"]}:{cfg["dev_port"]}'
        self.dummy_sock = ctx.socket(zmq.PAIR)
        self.dummy_sock.connect(dummy_uri)

    def start(self):
        self._alive = True
        self.sender_task = asyncio.ensure_future(self.sender())
        self.receiver_task = asyncio.ensure_future(self.receiver())

    async def sender(self):
        while self._alive:
            await self.dev_in_handler()

    async def receiver(self):
        while self._alive:
            await self.dev_out_handler()

    async def dev_in_handler(self):
        raw = await self.z_sock.recv_multipart()
        await self.dummy_sock.send_multipart(raw)

    async def dev_out_handler(self):
        raw = await self.dummy_sock.recv_multipart()
        await self.z_sock.send_multipart(raw)

    def stop(self):
        self._alive = False
        self.z_sock.close()
        self.sender_task.cancel()
        self.receiver_task.cancel()


class WebSocketsRunner:
    def __init__(self, ctx, uri_dev_io, proto, cfg):
        self.z_sock = ctx.socket(zmq.PAIR)
        self.z_sock.bind(uri_dev_io)

        self.ws_uri = f'ws://{cfg["dev_ip"]}:{cfg["dev_port"]}'
        self.ws_proto=proto

        self._alive = False

    def start(self):
        self._alive = True
        self.runner_task = asyncio.ensure_future(self.ws_handler())

    async def sender(self, websocket):
        while self._alive:
            packet = await self.dev_in_handler()
            await websocket.send(packet)

    async def receiver(self, websocket):
        while self._alive:
            async for msg in websocket:
                await self.dev_out_handler(websocket, msg)

    async def ws_handler(self):
        """ 'handles' websocket disconnect event
        don't trust this
        """
        counter = 0
        max_retry = 10
        while self._alive:
            if counter == max_retry:
                print('Connection lost... Terminating.')
                #self.stop() # ???
            try:
                counter = 0
                async with websockets.connect(
                                self.ws_uri,
                                create_protocol=self.ws_proto,
                                ping_interval=None,
                                ping_timeout=None,
                                compression=None) as websocket:
                    task_send = asyncio.Task(self.sender(websocket))
                    task_recv = asyncio.Task(self.receiver(websocket))
                    try:
                        await asyncio.gather(task_send, task_recv)
                    except Exception as e:
                        print(f'({self.ws_uri}) handler terminated -- Retry = {self._alive}')
                        #print('Reason: ', e)
                        task_send.cancel()
                        task_recv.cancel()
            except ConnectionRefusedError:
                counter += 1 # FIXME handle counter properly?
                #print(f'Disconnected, trying to reconnect... ({counter}/{max_retry})')
                await asyncio.sleep(1)

    async def dev_in_handler(self, websocket=None, msg=None):
        pass

    async def dev_out_handler(self, websocket=None, msg=None):
        pass

    def stop(self):
        self._alive = False
        self.z_sock.close()
        self.runner_task.cancel()
