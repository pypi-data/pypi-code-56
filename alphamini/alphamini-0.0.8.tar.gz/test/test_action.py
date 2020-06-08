import asyncio

from mini.blockapi.block_action import PlayAction, PlayActionResponse
from mini.blockapi.block_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.blockapi.block_action import GetActionList, GetActionListResponse, RobotActionType
from mini.blockapi.block_action import ChangeRobotVolume, ChangeRobotVolumeResponse
from mini.blockapi.base_api import BlockApiResultType

from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_play_action():
    block: PlayAction = PlayAction(action_name='018')
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_play_action timetout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'


async def test_move_robot():
    block: MoveRobot = MoveRobot(step=10, direction=MoveRobotDirection.LEFTWARD)
    (resultType, response) = await block.execute()

    print(f'test_move_robot result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


async def test_get_action_list():
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    (resultType, response) = await block.execute()

    print(f'test_get_action_list result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_get_action_list timetout'
    assert response is not None and isinstance(response,
                                               GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'


async def test_change_robot_volume():
    block: ChangeRobotVolume = ChangeRobotVolume(volume=0.5)
    (resultType, response) = await block.execute()

    print(f'test_change_robot_volume result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_change_robot_volume timetout'
    assert response is not None and isinstance(response,
                                               ChangeRobotVolumeResponse), 'test_change_robot_volume result unavailable'
    assert response.isSuccess, 'get_action_list failed'


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()
        await test_play_action()
        await test_move_robot()
        await test_get_action_list()
        await test_change_robot_volume()
        await shutdown()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    # device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    # if device:
    #     asyncio.get_event_loop().run_until_complete(test_connect(device))
    #     asyncio.get_event_loop().run_until_complete(test_start_run_program())
    #     asyncio.get_event_loop().run_until_complete(test_play_action())
    #     asyncio.get_event_loop().run_until_complete(test_move_robot())
    #     asyncio.get_event_loop().run_until_complete(test_get_action_list())
    #     asyncio.get_event_loop().run_until_complete(test_change_robot_volume())
    #     asyncio.get_event_loop().run_until_complete(shutdown())
