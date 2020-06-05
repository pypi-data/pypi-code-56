#!/usr/bin/env python3

from ..blockapi.base_api import BaseBlockApi, DEFAULT_TIMEOUT
from ..blockapi.cmdid import PCProgramCmdId
from ..pb2.codemao_controlbehavior_pb2 import ControlBehaviorRequest, ControlBehaviorResponse
from ..pb2.codemao_controlmouthlamp_pb2 import ControlMouthRequest, ControlMouthResponse
from ..pb2.codemao_playexpression_pb2 import PlayExpressionRequest, PlayExpressionResponse
from ..pb2.codemao_setmouthlamp_pb2 import SetMouthLampRequest, SetMouthLampResponse
from ..pb2.pccodemao_message_pb2 import Message


class PlayExpression(BaseBlockApi):
    """
    播放表情
    """

    def __init__(self, is_serial: bool = True, express_name: str = None, dir_type: int = 0):
        assert express_name is not None, 'PlayExpression expressName could not be None'
        self.__isSerial = is_serial
        self.__expressName = express_name
        self.__dirType = dir_type

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = PlayExpressionRequest()
        request.expressName = self.__expressName
        request.dirType = self.__dirType

        cmd_id: int = PCProgramCmdId.PLAY_EXPRESSION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayExpressionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ControlBehavior(BaseBlockApi):
    """
    控制表现力
    """

    # TODO 控制表现力接口， 如果event_type不传的话，实际调用到了停止表现力， event_type =0 是停止的意思
    def __init__(self, is_serial: bool = True, name: str = None, event_type: int = 1):
        assert name is not None, 'ControlBehavior name could not be None'
        self.__isSerial = is_serial
        self.__name = name
        self.__eventType = event_type

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = ControlBehaviorRequest()
        request.name = self.__name
        request.eventType = self.__eventType

        cmd_id = PCProgramCmdId.CONTROL_BEHAVIOR_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlBehaviorResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class SetMouthLamp(BaseBlockApi):
    """
    设置嘴巴灯
    """

    def __init__(self, is_serial: bool = True, model: int = 0, color: int = 0, duration: int = 0,
                 breath_duration: int = 0):

        self.__isSerial = is_serial
        self.__model = model
        self.__color = color
        self.__duration = duration
        self.__breathDuration = breath_duration

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = SetMouthLampRequest()
        request.model = self.__model
        request.color = self.__color
        request.duration = self.__duration
        request.breathDuration = self.__breathDuration

        cmd_id = PCProgramCmdId.SET_MOUTH_LAMP_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = SetMouthLampResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ControlMouthLamp(BaseBlockApi):
    """
    控制嘴巴灯开关
    """

    def __init__(self, is_serial: bool = True, is_open: bool = False):

        self.__isSerial = is_serial
        self.__isOpen = is_open

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = ControlMouthRequest()
        request.isOpen = self.__isOpen

        cmd_id = PCProgramCmdId.SWITCH_MOUTH_LAMP_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlMouthResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
