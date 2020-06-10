# -*- coding: utf-8 -*-


import asyncio
import atexit

import websockets

WSCLIENT = None


async def get_client():
    global WSCLIENT
    if WSCLIENT:
        return WSCLIENT


async def ws_sink(msg):
    print(msg)


async with websockets.connect(uri) as websocket:
    name = input("What's your name? ")

    await websocket.send(name)
    print(f"> {name}")

    greeting = await websocket.recv()
    print(f"< {greeting}")


class WsHandler:
    async def __call__(self):
        uri = "ws://localhost:8765"


@atexit.register
def shutdown(self):
    print("Shutting down Canvas...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(await_delete_channels())
    self.db.close()


async def await_delete_channels(self):
    # # Works but it is better to do it asynchronously
    # for ch in self.active_channels:
    #    await client.delete_channel(ch)
    #
    # Doing delete_channels() asynchronously
    delete_channels = [client.delete_channel(ch) for ch in self.active_channels]
    await asyncio.wait(delete_channels, return_when=asyncio.ALL_COMPLETED)
