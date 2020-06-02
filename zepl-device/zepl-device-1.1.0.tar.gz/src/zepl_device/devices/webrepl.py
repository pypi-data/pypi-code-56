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

class WebReplRunner(DeviceRunner):
    def __init__(self, dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out, cfg, fpath='./mpy-scripts/'):
        """WebReplDevice Implementatiton
        """
        super(WebReplRunner, self).__init__(dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out)

        self.cfg = cfg # ?? we could request this from a client

        self.ctrl_c = '\x03' # ctrl+c keyboard interrupt
        self.ctrl_d = '\x04' # ctrl+d soft reset

        # getting ugly
        if 'fpath' in cfg:
            self.mpy_dir = cfg['fpath']
        else:
            self.mpy_dir = fpath

        if 'init_sync' in cfg:
            self.init_sync = cfg['init_sync']
        else:
            self.init_sync = False

        if 'dev_mac' in cfg:
            self.mac = cfg['dev_mac'].encode()
        else:
            self.mac = None

        if 'sync_flist' in cfg:
            self.sync_flist = cfg['sync_flist']
        else:
            self.sync_flist = []

        if 'init_run' in cfg:
            self.init_run = cfg['init_run']
        else:
            self.init_run = False

    async def dev_in_handler(self):
        """handle controller requests
        """
        try:
            raw = await self.dev_in.recv_multipart()
            dev_id = raw.pop(0)
            route = raw.pop(0)
            dest = raw.pop(0)
        except Exception as e:
            print('WebReplRunner dev_in_handler failed: ', e)
            return

        if not dest == b'runner':
           return

        cmd = raw.pop(0)
        if cmd == b'greetings':
            resp = b'why hello there!'
        elif cmd == b'sync':
            await self.sync_files()
            resp = b'success'
        elif cmd == b'run':
            arg = raw.pop(0)
            await self.reset_run(arg.decode())
            resp = b'success'
        else:
            resp = b'err'

        try:
            await self.dev_out.send_multipart([dev_id, b'ctrl', route, resp])
        except Exception as e:
            print('dev_in sending failed: ', e)

    async def dev_out_handler(self):
        """state machine for device initialization + forwarding to broker
        """
        try:
            _, raw = await self.z_sock.recv_multipart()
            tag, msg = raw.decode().split(' ', 1)
            tag = tag.encode()
            msg = msg.encode()
        except Exception as e:
            #print('WebReplDevice dev_out dropping message: ', e)
            return

        # initial sync -> upload all in flist
        if self.init_sync:
            await self.sync_files()
            self.cfg['init_sync'] = False
            return
        # get machine mac
        if not self.mac:
            await self.get_mac()
            return
        # run after initialization
        if self.init_run:
            print(f'{self.dev_id} running initial app {self.init_run}')
            await self.reset_run(self.init_run)
            self.init_run=False
            return

        if tag not in [b'ERROR', b'LOG']: # filter
            return

        try:
            await self.dev_out.send_multipart([self.dev_id, b'log', tag, msg])
        except Exception as e:
            print('dev_in sending failed: ', e)

    async def send_seq(self, seq):
        for s in seq:
            await self.z_sock.send_multipart([b'c', s.encode()])
            await asyncio.sleep(.5) # FIXME this has to be larger than the poll timeout MP main.py

    async def upload_file(self, name):
        """upload single file to device
        """
        fname = self.mpy_dir+'/'+name # FIXME pls
        fsize = os.stat(fname)[6]
        try:
            with open(fname, 'rb') as fd:
                    data = fd.read(fsize)
            print(f'{self.dev_id} uploading file {name}')
            await self.z_sock.send_multipart([b'mp', b'put', name.encode(), f'{fsize}'.encode(), data])
        except Exception as e:
            print(e)

    async def sync_files(self):
        if self.init_sync:
            print('Performing initial upload...')
            for f in self.sync_flist:
                await self.upload_file(f)
            self.init_sync=False

        await self.reset_run('2')

        self.update_hashes()
        tag = None

        # FIXME hang forever
        while not tag == 'F_HTAB':
            try:
                raw = await self.z_sock.recv()
                tag, msg = raw.decode().split(' ', 1)
            except:
                continue

        remote = json.loads(msg)
        loc = self.cfg['loc_fhash']

        if not remote == loc:
            for f in self.sync_flist:
                if f in remote.keys():
                    if not remote[f] == loc[f]:
                        await self.upload_file(f)
                    else:
                        print(f'{self.dev_id} skipping upload of {f}')
                else:
                    await self.upload_file(f)

    async def get_mac(self):
        """seems to work all the time most of the time...
        """
        await self.reset_run('1')
        # FIXME hang forever
        while not self.mac:
            try:
                # FIXME duplicated often <-> subclass zmq socket TODO
                raw = await self.z_sock.recv()
                tag, msg = raw.decode().split(' ', 1)
                tag = tag.encode()
                msg = msg.encode()
            except:
                continue
            if tag == b'DEV_MAC':
                print(f'remote device mac address: {msg}')
                self.mac = msg
                break

    async def reset_run(self, app_id):
        """seems to work all the time most of the time...
        """
        await self.send_seq([self.ctrl_c, self.ctrl_d] )
        await asyncio.sleep(2) # zzz
        await self.send_seq([app_id])

    def update_hashes(self):
        """update table with filehashes
        """
        self.cfg['loc_fhash'] = {}
        for f in self.sync_flist:
            try:
                with open(self.mpy_dir+'/'+f, 'rb') as fd: # FIXME pls

                    hasher = hashlib.sha1()
                    data = fd.read()
                    hasher.update(data)
                    self.cfg['loc_fhash'][f] = binascii.hexlify(hasher.digest()).decode()
            except Exception as e:
                print('check your file list', e)
