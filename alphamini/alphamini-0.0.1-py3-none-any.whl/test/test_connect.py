import asyncio
import logging

import mini_sdk as MiniSdk
from blockapi.block_action import PlayAction
from channels import msg_utils
from dns.dns_browser import WiFiDevice
from pb2.codemao_playaction_pb2 import PlayActionResponse
from pb2.pccodemao_message_pb2 import Message


async def test_get_device_by_name():
    result = await MiniSdk.get_device_by_name("00090", 10)
    print(f"test_get_device_by_name1 result:{result}")
    return result


async def test_connect(dev: WiFiDevice):
    await MiniSdk.connect(dev)


async def shutdown():
    await asyncio.sleep(5)
    await MiniSdk.release()


async def send_msg():
    action = PlayAction(is_serial=True, action_name='dance_0001')
    result: Message = await action.execute()
    body = msg_utils.parse_body_msg(result.bodyData, PlayActionResponse)
    print(f'send_msg result:{body}')
    action2 = PlayAction(is_serial=True, action_name='dance_0002')
    result22: Message = await action2.execute()
    print(f'{result22}')


MiniSdk.set_log_level(logging.DEBUG)

if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(send_msg())
        asyncio.get_event_loop().run_until_complete(shutdown())
