#
# This file is part of zepl-device: https://gitlab.com/zepl1/zepl-device
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3

import os, hashlib, binascii
import json
import asyncio
import zmq.asyncio

from .runner import DeviceRunner

from pprint import pprint
import datetime as dt

class DummyBase:
    dummy_vals = {}
    tasks = {}

    def start_task(self, task_name, coro, sock, arg, prefix=[]):
        if coro == 'a':
            self.tasks[task_name] = asyncio.ensure_future(self.coro_a(sock, arg, prefix))
        elif coro == 'b':
            self.tasks[task_name] = asyncio.ensure_future(self.coro_b(sock, arg, prefix))

    def stop_task(self, task_name):
        self.tasks[task_name].cancel()

    async def coro_a(self, sock, arg, prefix):
        msg = prefix
        msg.append(f'coro_a {arg}'.encode())
        while True:
            await asyncio.sleep(1)
            sock.send_multipart(msg)

    async def coro_b(self, sock, arg, prefix):
        msg = prefix
        msg.append(f'coro_b {arg}'.encode())
        while True:
            await asyncio.sleep(3)
            sock.send_multipart(msg)


class DummyRunner(DeviceRunner, DummyBase):
    def __init__(self, dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out, cfg):
        """DummyRunner
        """
        super(DummyRunner, self).__init__(dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out)

    async def dev_in_handler(self):
        """handle controller requests
        """
        try:
            raw = await self.dev_in.recv_multipart()
            dev_id = raw.pop(0)
            route = raw.pop(0)
            dest = raw.pop(0)
        except Exception as e:
            print('DummyRunner dev_in_handler failed: ', e)
            return

        if not dest == b'runner':
            resp = b'not sure if...'
            await self.z_sock.send_multipart(raw)
            await self.dev_out.send_multipart([dev_id, b'ctrl', route, resp])
            return

        raw = [s.decode() for s in raw]
        cmd = raw.pop(0)
        if cmd == 'greetings':
            resp = b'why hello there!'
        elif cmd == 'start':
            task_name = raw.pop(0)
            coro_id = raw.pop(0)
            args = json.loads(raw.pop(0))
            self.start_task(task_name, coro_id, self.dev_out, args, prefix=[dev_id, b'log', b'DUMMY_RUNNER_RAW_OUT'])
            resp = b'starting coro!'
        elif cmd == 'stop':
            task_name = raw.pop(0)
            self.stop_task(task_name)
            resp = b'stopping coro!'
        else:
            resp = b'err'

        try:
            await self.dev_out.send_multipart([dev_id, b'ctrl', route, resp])
        except Exception as e:
            print('DummyRunner dev_in sending failed: ', e)

    async def dev_out_handler(self):
        """
        """
        try:
            raw = await self.z_sock.recv()
            #print(f'DummyRunner forwarding FROM device {raw}')
            msg = [self.dev_id, b'log', b'DUMMY_DEV_RAW_OUT', raw]
            await self.dev_out.send_multipart(msg)
        except Exception as e:
            print(f'DummyRunner dev_out_handler failed: {e}')

class DummyDevice(DummyBase):
    def __init__(self, ctx, cfg):
        dummy_uri = f'tcp://0.0.0.0:{cfg["dev_port"]}'
        self.dummy_sock = ctx.socket(zmq.PAIR)
        self.dummy_sock.bind(dummy_uri)

    def start(self):
        self._alive = True
        self.dev_in_task = asyncio.ensure_future(self.dev_in_loop())

    async def dev_in_loop(self):
        while self._alive:
            try:
                raw = await self.dummy_sock.recv_multipart()
                raw = [s.decode() for s in raw]
            except Exception as e:
                print('DummyDevice dev_in_loop failed: ', e)
                return

            #print(f'A DummyDevice received: {raw}')
            cmd = raw.pop(0)
            if cmd == 'greetings':
                resp = b'why hello there!'
            elif cmd == 'start':
                task_name = raw.pop(0)
                coro_id = raw.pop(0)
                args = json.loads(raw.pop(0))
                self.start_task(task_name, coro_id, self.dummy_sock, args, prefix=[])
                resp = b'starting coro!'
            elif cmd == 'stop':
                task_name = raw.pop(0)
                self.stop_task(task_name)
                resp = b'stopping coro!'
            else:
                resp = b'err'

            try:
                await self.dummy_sock.send_multipart([resp])
            except Exception as e:
                print('DummyDevice sending failed: ', e)

    def stop(self):
        self._alive = False
        self.dummy_sock.close()
        self.dev_in_task.cancel()
