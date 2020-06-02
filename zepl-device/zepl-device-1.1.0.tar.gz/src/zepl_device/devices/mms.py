#
# This file is part of zepl-device: https://gitlab.com/zepl1/zepl-device
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3

import os, hashlib, binascii
import json
import asyncio
import zmq.asyncio
from pathlib import Path

from .runner import DeviceRunner

from pprint import pprint
import datetime as dt

FILES_DEFAULT = {
    'lib': [],
    'root': [ 'boot.py', 'main.py', 'board.py' ],
    'config': [ 'board.json', 'wifi.secret' ]
}

class MmsRunner(DeviceRunner):
    def __init__(self, dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out, cfg, files=FILES_DEFAULT):
        """WebReplDevice Implementatiton
        """
        super(MmsRunner, self).__init__(dev_id, ctx, uri_dev_io, uri_dev_in, uri_dev_out)

        self.ctrl_c = '\x03' # ctrl+c keyboard interrupt
        self.ctrl_d = '\x04' # ctrl+d soft reset

        self.update_config(cfg) # ?? do not instantiate -> make it mutable from client side

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

        while self.uploading or self.initializing:
            await asyncio.sleep(1)

        if not dest == b'runner':
           return

        #print('INBOUND', dev_id, route, dest, raw)

        cmd = raw.pop(0)
        if cmd == b'greetings':
            resp = b'why hello there!'
        elif cmd == b'info':
            resp = json.dumps({'info': 'test'})
        elif cmd == b'sync':
            await self.sync_files()
            resp = b'success'
        elif cmd == b'run':
            arg = raw.pop(0)
            await self.reset_run(arg.decode())
            resp = b'success'
        elif cmd == b'send':
            msg = raw.pop(0)
            await self.z_sock.send_multipart([b'c', msg])
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
        while self.uploading:
            await asyncio.sleep(1)
        try:
            _, raw = await self.z_sock.recv_multipart()
            tag, msg = raw.decode().split(' ', 1)
            tag = tag.encode()
            msg = msg.encode()
        except Exception as e:
            #print('WebReplDevice dev_out dropping message: ', e)
            return

        #print('OUTBOUND', tag, msg)

        # initial sync -> upload all files
        if self.init_sync:
            await self.sync_files()
            self.init_sync = False

        # run app as last step of initialization
        if self.initializing:
            print(f'{self.dev_id} running initial app {self.init_run}')
            await self.reset_run(self.init_run)
            self.initializing = False
            return

        if tag not in [b'ERROR', b'LOG', b'DATA']: # filter
            return

        try:
            await self.dev_out.send_multipart([self.dev_id, b'log', tag, msg])
        except Exception as e:
            print('dev_in sending failed: ', e)

    async def send_seq(self, seq):
        for s in seq:
            await self.z_sock.send_multipart([b'c', s.encode()])
            await asyncio.sleep(0.5) # FIXME this has to be larger than the poll timeout MP main.py

    async def reset_run(self, app_id):
        """seems to work all the time most of the time...
        """
        await self.send_seq([self.ctrl_c, self.ctrl_d])
        await asyncio.sleep(3.5) # zzz
        await self.send_seq([app_id])

    async def upload_file(self, d, name):
        """upload single file to device
        """
        l_file = Path('./') / d / name
        r_path = None
        if d == 'lib':
           r_path = '/lib/'+name
        else:
           r_path = '/'+name
        fsize = os.stat(l_file)[6]
        try:
            with open(l_file, 'rb') as fd:
                    data = fd.read(fsize)
            print(f'{self.dev_id} uploading file {name}')
            await self.z_sock.send_multipart([b'mp', b'put', r_path.encode(), f'{fsize}'.encode(), data])
        except Exception as e:
            print(e)

    async def sync_files(self):
        self.uploading = True
        if self.init_sync:
            print('Performing initial upload...')
            for d in self.files.keys():
                for f in self.files[d]:
                    await self.upload_file(d, f)
            self.uploading = False
            return

        await self.reset_run('2')

        self.update_hashes()
        tag = None

        # FIXME hang forever
        while not tag == 'F_HTAB':
            try:
                _, raw = await self.z_sock.recv_multipart()
                tag, msg = raw.decode().split(' ', 1)
                #print('wait sync', raw)
            except:
                #print('fail sync', raw)
                continue

        remote = json.loads(msg)

        #print("")
        #print('REMOTE')
        #pprint(remote)
        #print("")
        #print('LOCAL')
        #pprint(self.loc_fhash)
        #print("")

        if not remote == self.loc_fhash:
            for d in self.files.keys():
                for f in self.files[d]:
                    if d == 'lib':
                        name = '/lib/'+f
                    else:
                        name = f
                    if name in remote.keys():
                        if not remote[name] == self.loc_fhash[name]:
                            await self.upload_file(d, f)
                        else:
                            print(f'{self.dev_id} skipping upload of {f}')
                    else:
                        await self.upload_file(d, f)

        print(f'Synchronized -> reset run: {self.init_run}!')
        await self.reset_run(self.init_run)
        self.uploading = False

    def update_hashes(self):
        """update table with filehashes
        """
        self.loc_fhash = {}
        for d in self.files.keys():
            for f in self.files[d]:
                l_file = Path('./') / d / f
                if d == 'lib':
                    hash_key = '/lib/'+f
                else:
                    hash_key = f
                try:
                    with open(l_file, 'rb') as fd:
                        hasher = hashlib.sha1()
                        data = fd.read()
                        hasher.update(data)
                        self.loc_fhash[hash_key] = binascii.hexlify(hasher.digest()).decode()
                except Exception as e:
                    print('check your file list', e)

    def update_config(self, cfg):
        """ getting ugly....
        """
        self.initializing = True
        self.uploading = False
        self.init_sync = cfg['init_sync']
        self.init_run = cfg['init_run']

        if 'files' in cfg:
            self.files = cfg['files']
        else:
            self.files = []

