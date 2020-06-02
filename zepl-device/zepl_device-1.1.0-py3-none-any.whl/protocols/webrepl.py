#!/usr/bin/env python
#
# Micropython Websockets Protocol
# implemented on top of websockets
# there is an argument called 'subprotocol' available for websockets connections
# didn't figure that one out...
# some of the WebReplProto class ist copy pasted from websockets
#
# This file is part of zepl-device: https://gitlab.com/zepl1/zepl-device
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3.0-or-later

import os
import struct
import asyncio

from typing import (
    AsyncIterable,
    Iterable,
    Union,
    cast,
)

from websockets.client import WebSocketClientProtocol
from websockets.typing import Data, Optional
from websockets.framing import *

from .runner import WebSocketsRunner
from pprint import pprint

def mp_codec(cdc, name, size=None):
    """\
        Micropython WebREPL <-> zmq codec
    mode       | cdc | name |size|  webrepl
    ===========|=====|======|====|=======================================================================
    char       |  c  | ---- |None|  no special treatment needed
    -----------|-----|------|----|-----------------------------------------------------------------------
    command    | cmd |b'ver'| -- |  currently only b'ver' is a valid command
    -----------|-----|------|----|-----------------------------------------------------------------------
    send_file  | put |fname | sz | FIXME only sending as single chunk -> next message part is the payload
    -----------|-----|------|----|-----------------------------------------------------------------------
    get_file   | get |fname | -- | synchronous request<->reply control flow
    -----------|-----|------|----|-----------------------------------------------------------------------

    technically this butchered version should not work
    """
    WEBREPL_PKT_FMT = "<sBBQLH64s"
    WEBREPL_PKT_PREFIX = b"W"
    WEBREPL_OPCODE_PUT_FILE = 0x01
    WEBREPL_OPCODE_GET_FILE = 0x02
    WEBREPL_OPCODE_GET_VER  = 0x03

    fn = name
    sz = 0

    if cdc == b'get':
        opcode = WEBREPL_OPCODE_GET_FILE

    elif cdc == b'put':
        opcode = WEBREPL_OPCODE_PUT_FILE
        sz = size if size else 0

    elif cdc == b'cmd':
        if name == b'ver':
            opcode = WEBREPL_OPCODE_GET_VER
            fn = b''
        else:
            raise NotImplementedError(f"codec(cmd): '{name}' no comprende!")
    else:
        raise NotImplementedError("codec does not understand!")

    # assemble packet
    packet = struct.pack(
            WEBREPL_PKT_FMT,
            WEBREPL_PKT_PREFIX,
            opcode,
            0, 0, sz, len(fn), fn)

    return packet

class WebReplProto(WebSocketClientProtocol):
    mp_wait    = False
    mp_codec   = False
    mp_version = False
    mp_download= False

    async def send(
        self, message: Union[Data, Iterable[Data], AsyncIterable[Data]]
    ) -> None:
        """
        This coroutine sends a message.
        """
        await self.ensure_open()

        # Unfragmented message -- this case must be handled first because
        # strings and bytes-like objects are iterable.

        if isinstance(message, (str, bytes, bytearray, memoryview)):
            opcode, data = prepare_data(message)
            #print(opcode, data, len(data))
            await self.write_frame(True, opcode, data)

        # Fragmented message -- regular iterator.

        elif isinstance(message, Iterable):

            # Work around https://github.com/python/mypy/issues/6227
            message = cast(Iterable[Data], message)

            iter_message = iter(message)

            # First fragment.
            try:
                message_chunk = next(iter_message)
            except StopIteration:
                return

            # micropython webrepl hackery
            if message_chunk == b'mp':
                opcode = 2
                delaaay = 0.1

                cmd = next(iter_message)
                name = next(iter_message)
                packet = mp_codec(cmd, name)

                if cmd == b'cmd':
                    self.mp_version = True
                    await self.write_frame(True, opcode, packet)
                    await asyncio.sleep(delaaay)
                    await self.write_frame(True, opcode, b'\x00')

                elif cmd == b'get':
                    await self.write_frame(True, opcode, packet)
                    self.mp_download = True
                    self.mp_wait = True
                    # false if '\x00\x00' is received
                    while self.mp_download:
                        await asyncio.sleep(delaaay)

                        # gets reset everytime a frame is received
                        if not self.mp_wait:
                            await self.write_frame(True, opcode, b'\x00')
                            self.mp_wait = True

                elif cmd == b'put':
                    size = next(iter_message)
                    packet = mp_codec(cmd, name, int(size.decode()))
                    await self.write_frame(True, opcode, packet[:10])

                    await asyncio.sleep(delaaay)
                    await self.write_frame(True, opcode, packet[10:])

                    await asyncio.sleep(delaaay)
                    # FIXME send in chunks?
                    data = next(iter_message)
                    await self.write_frame(True, opcode, data)

                    await asyncio.sleep(delaaay)
                    await self.write_frame(True, opcode, b'\x00')

        else:
            raise TypeError("data must be bytes, str, or iterable")

    async def read_data_frame(self, max_size: Optional[int]) -> Optional[Frame]:
        """
        Read a single data frame from the connection.
        Process control frames received before the next data frame.
        Return ``None`` if a close frame is encountered before any data frame.
        """
        # 6.2. Receiving Data
        while True:
            frame = await self.read_frame(max_size)

            # MP download snychronization
            self.mp_wait = False

            # convert version format to string
            if self.mp_version:
                try:
                    data = f'\nMP Version: {struct.unpack("<BBB", frame.data)}\n>>> '
                except:
                    data = 'Error getting version!\n'
                self.mp_version = False
                return Frame(True, 2, data)

            # if this frame gets lost the sender will be stuck in the download loop
            if frame.data == b'\x00\x00':
                self.mp_download = False

            # these frames are signalling success, we silence them
            if frame.data == b'WB\x00\x00':
                return Frame(True, 2, '')


            # 5.5. Control Frames
            if frame.opcode == OP_CLOSE:
                # 7.1.5.  The WebSocket Connection Close Code
                # 7.1.6.  The WebSocket Connection Close Reason
                self.close_code, self.close_reason = parse_close(frame.data)
                try:
                    # Echo the original data instead of re-serializing it with
                    # serialize_close() because that fails when the close frame
                    # is empty and parse_close() synthetizes a 1005 close code.
                    await self.write_close_frame(frame.data)
                except ConnectionClosed:
                    # It doesn't really matter if the connection was closed
                    # before we could send back a close frame.
                    pass
                return None

            # 5.6. Data Frames
            else:
                return frame

class WebReplIo(WebSocketsRunner):
    def __init__(self, ctx, uri_dev_io, cfg):
        super(WebReplIo, self).__init__(ctx, uri_dev_io, WebReplProto, cfg)
        self.password = cfg['dev_pw']

    async def dev_in_handler(self):
        raw = await self.z_sock.recv_multipart()
        send_mode = raw[0]
        if not send_mode == b'c':
            packet = raw
        else:
            packet = raw[1].decode() # bytearray gets gets sent as text frame by websockets
        #print(f'WebReplIo send: "{packet}"')
        return packet

    async def dev_out_handler(self, websocket, msg):
        # login automatically
        if self.password:
            if msg == 'Password: ':
                await websocket.send(f'{self.password}\r\n'.encode())
                #self.password=None # login (only once?)
                return

        #print(f'WebReplIo recv: "{msg}"')
        if isinstance(msg, str):
            await self.z_sock.send_multipart([b's', msg.encode()])
        else:
            await self.z_sock.send_multipart([b'b', msg])
