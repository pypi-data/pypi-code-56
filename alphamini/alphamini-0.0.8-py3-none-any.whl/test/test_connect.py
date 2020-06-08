import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.blockapi.block_setup import StartRunProgram
from mini.dns.dns_browser import WiFiDevice


async def test_get_device_by_name():
    result = await MiniSdk.get_device_by_name("00018", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


async def test_connect(dev: WiFiDevice):
    await MiniSdk.connect(dev)


async def test_start_run_program():
    await StartRunProgram().execute()
    await asyncio.sleep(6)


async def shutdown():
    await asyncio.sleep(1)
    await MiniSdk.release()


MiniSdk.set_log_level(logging.INFO)

if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(shutdown())
