import asyncio
import logging

import mini_sdk as MiniSdk
from blockapi.block_setup import StartRunProgram, StopRunProgram
from dns.dns_browser import WiFiDevice


async def test_get_device_by_name():
    result = await MiniSdk.get_device_by_name("00022", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


async def test_connect(dev: WiFiDevice):
    await MiniSdk.connect(dev)


async def test_start_run_program():
    await StartRunProgram().execute()


async def shutdown():
    await asyncio.sleep(5)
    await MiniSdk.release()


MiniSdk.set_log_level(logging.INFO)

if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(shutdown())
