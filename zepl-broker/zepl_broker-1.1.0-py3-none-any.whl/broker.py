#
# This file is part of Zepl Broker: https://gitlab.com/zepl1/zepl-broker
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3
import json
import asyncio
import zmq.asyncio
from pprint import pprint

from zepl_device import ZeplDevice

class ZeplBroker():
    uri_dev_in = 'inproc://dev_in'
    uri_dev_out = 'inproc://dev_out'

    ctx = zmq.asyncio.Context(io_threads=4)

    dev_out = ctx.socket(zmq.SUB)
    dev_out.bind(uri_dev_out)
    dev_out.subscribe(b'')

    dev_in = ctx.socket(zmq.PUB)
    dev_in.bind(uri_dev_in)

    log_out = ctx.socket(zmq.PUB)
    device = ctx.socket(zmq.ROUTER)
    ctrl = ctx.socket(zmq.ROUTER)

    _alive = False

    def __init__(self, cfg=None, uri_log_out='tcp://0.0.0.0:9000', uri_device='tcp://0.0.0.0:9001', uri_ctrl='tcp://0.0.0.0:9002'):
        self.loop = asyncio.get_event_loop()
        self.log_out.bind(uri_log_out)
        self.device.bind(uri_device)
        self.ctrl.bind(uri_ctrl)
        self.dev_map = {}

    def start(self):
        self._alive = True
        self.ctrl_task = asyncio.ensure_future(self.broker_switch())

    def add_device(self, dev_id, cfg):
        try:
            device = ZeplDevice(self.ctx, dev_id, self.uri_dev_in, self.uri_dev_out, cfg)
        except Exception as e:
            print(e)
        device.start()
        self.dev_map[dev_id] = device

    def remove_device(self, dev):
        """collect garbage?
        """
        self.dev_map[dev].stop()
        del self.dev_map[dev]

    async def broker_switch(self):
        poller = zmq.asyncio.Poller()
        poller.register(self.dev_out, zmq.POLLIN)
        poller.register(self.device, zmq.POLLIN)
        poller.register(self.ctrl, zmq.POLLIN)

        self._alive = True
        while self._alive:
            socks = dict(await poller.poll(100))

            if self.device in socks.keys():
                try:
                    raw = await self.device.recv_multipart()
                    raw[0], raw[1] = raw[1], raw[0]
                    await self.dev_in.send_multipart(raw)
                except Exception as e:
                    print(f'broker(device) dropping msg: {raw} -- {e}')

            if self.dev_out in socks.keys():
                try:
                    topic, msg_type, prefix, msg = await self.dev_out.recv_multipart()
                except Exception as e:
                    print(f'broker(dev_out) dropping msg: {raw} -- {e}')

                if msg_type == b'log':
                    await self.log_out.send_multipart([topic, prefix, msg])
                elif msg_type == b'ctrl':
                    await self.device.send_multipart([prefix, msg])
                else:
                    #print(f'broker(dev_out) dropping msg: {topic}{msg_type}{raw}')
                    pass

            if self.ctrl in socks.keys():
                try:
                    raw = await self.ctrl.recv_multipart()
                    resp = self.ctrl_handler(raw)
                    await self.ctrl.send_multipart(resp)
                except Exception as e:
                    print(f'broker(ctrl) dropping msg: {raw} -- {e}')

    def ctrl_handler(self, raw):
        route = raw.pop(0)
        cmd = raw.pop(0)
        if cmd == b'get':
            resp = [d.encode() for d in self.dev_map]
            if len(resp) == 0:
                resp = b'no devices active'
        elif cmd == b'add':
            try:
                dev_id = raw.pop(0)
                cfg = json.loads(raw.pop(0).decode())
                self.add_device(dev_id.decode(), cfg)
                resp = b'success'
            except:
                resp = b'error adding device'
        elif cmd == b'rem':
            try:
                d = raw.pop(0).decode()
                self.remove_device(d)
                resp = b'success'
            except:
                resp = b'error removing device'
        else:
            resp = b'unknown cmd'
        if isinstance(resp, bytes):
            resp = [route, resp]
        else:
            resp = [route, *resp]
        return resp

    def stop(self):
        self._alive = False
        devs = [d for d in self.dev_map.keys()]
        for d in devs:
            self.remove_device(d)
        self.ctrl_task.cancel()
