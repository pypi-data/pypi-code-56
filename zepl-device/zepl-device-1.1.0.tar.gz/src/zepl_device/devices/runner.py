# This file is part of zepl-device: https://gitlab.com/zepl1/zepl-device
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3

import asyncio
import zmq.asyncio

from pprint import pprint

class DeviceRunner:
    def __init__(self, dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out):
        """runner base class
        """
        self.z_sock = ctx.socket(zmq.PAIR)
        self.z_sock.connect(uri_dev_io)

        # FIXME encode so we can use as msgpart
        # -> zepl context is needed!
        self.dev_id = dev_id.encode()

        self.dev_in = ctx.socket(zmq.SUB)
        self.dev_in.connect(uri_dev_in)
        self.dev_in.subscribe(dev_id.encode())

        self.dev_out = ctx.socket(zmq.PUB)
        self.dev_out.connect(uri_dev_out)

        self._alive = False

    def start(self):
        self._alive = True
        self.dev_in_task = asyncio.ensure_future(self.sender())
        self.dev_out_task = asyncio.ensure_future(self.receiver())

    async def sender(self):
        while self._alive:
            await self.dev_in_handler()

    async def receiver(self):
        while self._alive:
            await self.dev_out_handler()

    async def dev_in_handler(self):
        """to be overridden by child
        """
        try:
            raw = await self.dev_in.recv_multipart()
            raw.pop(0) # strip topic
            print(f'DeviceRunner forwarding TO device {raw}')
            await self.z_sock.send_multipart(raw)
        except Exception as e:
            print(f'DeviceRunner dev_in_handler failed: {e}')

    async def dev_out_handler(self):
        """to be overridden by child
        """
        try:
            raw = await self.z_sock.recv()
            print(f'DeviceRunner forwarding FROM device {raw}')
            msg = [self.dev_id, b'log', b'DEV_RUNNER_RAW', raw]
            await self.dev_out.send_multipart(msg)
        except Exception as e:
            print(f'DeviceRunner dev_out_handler failed: {e}')

    def stop(self):
        self._alive = False
        self.z_sock.close()
        self.dev_in.close()
        self.dev_out.close()
        self.dev_in_task.cancel()
        self.dev_out_task.cancel()
