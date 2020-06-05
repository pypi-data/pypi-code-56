import asyncio

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from blockapi.block_action import PlayAction, MoveRobot
from dns.dns_browser import WiFiDevice
from test.test_connect import test_get_device_by_name, test_start_run_program, test_stop_run_program
from test.test_connect import test_connect, shutdown


async def test_play_action():
    block: PlayAction = PlayAction(action_name='dance_0002')
    response = await block.execute()
    print(f'test_play_action: {response}')


async def test_move_robot():
    block: MoveRobot = MoveRobot(step=10, direction=1)
    response = await block.execute()
    print(f'test_move_robot: {response}')


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_action())
        asyncio.get_event_loop().run_until_complete(test_move_robot())
        asyncio.get_event_loop().run_until_complete(shutdown())
