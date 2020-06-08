import asyncio

from mini.blockapi import errors
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name

from mini.blockapi.base_api import BlockApiResultType
from mini.blockapi.block_expression import PlayExpression, PlayExpressionResponse, RobotExpressionType
from mini.blockapi.block_expression import ControlBehavior, ControlBehaviorResponse, RobotBehaviorControlType
from mini.blockapi.block_expression import SetMouthLamp, SetMouthLampResponse, MouthLampColor
from mini.blockapi.block_expression import ControlMouthLamp, ControlMouthResponse


async def test_play_expression():
    block: PlayExpression = PlayExpression(express_name="codemao1", express_type=RobotExpressionType.INNER)
    (resultType, response) = await block.execute()

    print(f'test_play_expression result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_play_expression timetout'
    assert response is not None and isinstance(response,
                                               PlayExpressionResponse), 'test_play_expression result unavailable'
    assert response.isSuccess, 'play_expression failed'


async def test_control_behavior():
    block: ControlBehavior = ControlBehavior(name="dance_0004", control_type=RobotBehaviorControlType.START)
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    print(
        'resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

    assert resultType == BlockApiResultType.Success, 'test_control_behavior timetout'
    assert response is not None and isinstance(response,
                                               ControlBehaviorResponse), 'test_control_behavior result unavailable'
    assert response.isSuccess, 'control_behavior failed'


async def test_set_mouth_lamp():
    block: SetMouthLamp = SetMouthLamp(color=MouthLampColor.GREEN, model=0, duration=-1, breath_duration=1000)
    (resultType, response) = await block.execute()

    print(f'test_set_mouth_lamp result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_set_mouth_lamp timetout'
    assert response is not None and isinstance(response, SetMouthLampResponse), 'test_set_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'set_mouth_lamp failed'


async def test_control_mouth_lamp():
    (resultType, response) = await ControlMouthLamp(is_open=True).execute()

    print(f'test_control_mouth_lamp result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_control_mouth_lamp timetout'
    assert response is not None and isinstance(response,
                                               ControlMouthResponse), 'test_control_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'control_mouth_lamp failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_expression())
        asyncio.get_event_loop().run_until_complete(test_set_mouth_lamp())
        asyncio.get_event_loop().run_until_complete(test_control_mouth_lamp())
        asyncio.get_event_loop().run_until_complete(test_control_behavior())
        asyncio.get_event_loop().run_until_complete(shutdown())
