#
# This file is part of zepl-device: https://gitlab.com/zepl1/zepl-device
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3

import zmq.asyncio

class ZeplDevice:
    def __init__(self, ctx, dev_id, uri_dev_in, uri_dev_out, cfg):
        """assemble zepl device class
        passing the context enables the use of inproc transport

        dev_id: has to be unique in its context used as uri for DeviceRunner/DeviceIo
                devices and protocols will need be handled in same process and context
        uri_dev_in: sub socket broker->device
        uri_dev_out: pub socker device->broker
        """
        uri_dev_io = f'inproc://{dev_id}'

        for x in ['dev_type', 'dev_ip', 'dev_port','dev_pw']:
            if x not in cfg.keys():
                raise ValueError(f'you need to specify {x} in your config.')

        dev_type = cfg['dev_type']

        if dev_type == 'webrepl-example':
            from .devices.webrepl import WebReplRunner
            from .protocols.webrepl import WebReplIo
            dev_runner = WebReplRunner(dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out, cfg)
            io_runner = WebReplIo(ctx, uri_dev_io, cfg)
            self.runners = [dev_runner, io_runner]
        elif dev_type == 'dummy-example':
            from .devices.dummy import DummyRunner
            from .protocols.dummy import DummyIo
            dev_runner = DummyRunner(dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out, cfg)
            io_runner = DummyIo(ctx, uri_dev_io, cfg)
            self.runners = [dev_runner, io_runner]
        if dev_type == 'mms':
            from .devices.mms import MmsRunner
            from .protocols.webrepl import WebReplIo
            dev_runner = MmsRunner(dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out, cfg)
            io_runner = WebReplIo(ctx, uri_dev_io, cfg)
            self.runners = [dev_runner, io_runner]
        else:
            raise NotImplementedError(f'Zepl Device type "{dev_type}" not implemented')

        print('ZeplDevice initialized.')

    def start(self):
        """ start runners
        """
        for runner in self.runners:
            runner.start()

    def stop(self):
        """ stop runners
        """
        for runner in self.runners:
            runner.stop()
