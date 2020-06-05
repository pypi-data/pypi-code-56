import asyncio

from blockapi.block_expression import PlayExpression, ControlBehavior, SetMouthLamp, ControlMouthLamp
from dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name


async def test_play_expression():
    block: PlayExpression = PlayExpression(express_name="dance_0002")
    response = await block.execute()
    print(f'test_play_expression: {response}')


async def test_control_behavior():
    block: ControlBehavior = ControlBehavior(name="dance_0002")
    response = await block.execute()
    print(f'test_control_behavior: {response}')


async def test_set_mouth_lamp():
    block: SetMouthLamp = SetMouthLamp(color=1, duration=5000)
    response = await block.execute()
    print(f'test_set_mouth_lamp: {response}')


async def test_switch_mouth_lamp():
    response = await ControlMouthLamp(is_open=True).execute()
    print(f'test_switch_mouth_lamp: {response}')


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_expression())
        asyncio.get_event_loop().run_until_complete(test_control_behavior())
        asyncio.get_event_loop().run_until_complete(test_set_mouth_lamp())
        asyncio.get_event_loop().run_until_complete(test_switch_mouth_lamp())
        asyncio.get_event_loop().run_until_complete(shutdown())
