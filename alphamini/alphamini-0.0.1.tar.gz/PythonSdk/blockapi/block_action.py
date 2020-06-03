#!/usr/bin/env python3

from blockapi.base_api import BaseBlockApi, DEFAULT_TIMEOUT
from blockapi.cmdid import PCProgramCmdId
from pb2.pccodemao_message_pb2 import Message

from pb2.codemao_playaction_pb2 import *
from pb2.codemao_stopaction_pb2 import *
from pb2.codemao_moverobot_pb2 import *


class PlayAction(BaseBlockApi):
    """
    执行动作
    默认串行
    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        assert action_name is not None, 'actionName could not be None'
        self.__isSerial = is_serial
        self.__actionName = action_name

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = PlayActionRequest()
        request.actionName = self.__actionName

        cmd_id = PCProgramCmdId.PLAY_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAction(BaseBlockApi):

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = StopActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = StopActionRequest()
        cmd_id = PCProgramCmdId.STOP_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)


class MoveRobot(BaseBlockApi):

    def __init__(self, is_serial: bool = True, direction: int = None, step: int = None):
        assert direction is not None and direction > 0, 'direction should not be None,and should be Positive'
        assert step is not None and step > 0, 'step should not be None,and should be Positive'
        self.__isSerial = is_serial
        self.__direction = direction
        self.__step = step

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = MoveRobotResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = MoveRobotRequest()
        request.direction = self.__direction
        request.step = self.__step
        cmd_id = PCProgramCmdId.MOVE_ROBOT_REQUEST.value
        return await self.send(cmd_id, request, timeout)
