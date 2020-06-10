# -*- coding: utf-8 -*-

import asyncio
import atexit

import httpx

HTTP_CLIENT = httpx.AsyncClient()

# async def get_client():
#     HTTP_CLIENT


async def http_sink(msg):
    print(msg)


@atexit.register
def shutdown(self):
    print("Shutting down")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(await_delete_channels())


async def await_delete_channels(self):
    await HTTP_CLIENT.aclose()
