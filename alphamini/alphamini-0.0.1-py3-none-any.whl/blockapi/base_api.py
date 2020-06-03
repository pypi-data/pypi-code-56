#!/usr/bin/env python3
import abc
import asyncio
import enum
import os
import sys
from abc import ABC
from typing import Callable

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from pb2.pccodemao_message_pb2 import Message
from pb2.codemao_controltts_pb2 import ControlTTSRequest
from pb2.codemao_speechrecognise_pb2 import SpeechRecogniseRequest, SpeechRecogniseResponse
from channels.websocket_client import ubt_websocket as _UBTWebSocket
from channels.websocket_client import DefaultMsgHandler

DEFAULT_TIMEOUT = 300

socket = _UBTWebSocket()


@enum.unique
class BlockApiResultType(enum.Enum):
    Success = 1
    Timeout = 2


@enum.unique
class BlockEventType(enum.Enum):
    FaceReco = 1
    ASR = 2
    ASROffline = 3


class BaseBlockApi(abc.ABC):
    """
    积木块消息api基类
    向机器人发送消息
    """

    async def send(self, cmd_id: int, message, timeout: int) -> object:
        print('BaseBlockApi send start: cmdId:{},message:{}'.format(str(cmd_id), message))

        assert cmd_id >= 0, 'cmdId should not be negative number in BaseBlockApi'
        assert message is not None, 'message should not be none in BaseBlockApi'
        # 通用的发送消息逻辑
        if timeout <= 0:
            # 无超时，不需要回复
            asyncio.create_task(socket.send_msg(cmd_id, message, timeout))
            return None
        else:
            result = await socket.send_msg(cmd_id, message, timeout)

            # #test：模拟返回值
            #
            # await asyncio.sleep(3)
            #
            # result = (BlockApiResultType.Success, 'cmd:{}'.format(cmdId))

            # TODO:判断成功还是失败
            return result

    async def execute(self):
        raise NotImplementedError()

    # 解析业务message
    def parse_msg(self, message):
        raise NotImplementedError()


class BaseBlockApiNeedResponse(BaseBlockApi, abc.ABC):
    """
    积木块消息api基类
    向机器人发送消息
    需要回复，timeout不能为空
    """

    async def send(self, cmd_id, data, timeout: int):
        print('BaseBlockApiNeedResponse send')
        assert timeout > 0, 'timeout should be Positive number in BaseBlockApiNeedResponse'
        return await super().send(cmd_id, data, timeout)


class BaseBlockApiNoNeedResponse(BaseBlockApi, ABC):
    """
    积木块消息api基类
    向机器人发送消息
    不需要需要回复
    """

    async def send(self, cmd_id, message, timeout: int = 0):
        # 默认timeout为0
        return await super().send(cmd_id, message, 0)


class BaseEventApi(BaseBlockApiNoNeedResponse, DefaultMsgHandler, ABC):
    """
    事件类消息api基类
    """

    def __init__(self, cmd_id: int, message, is_repeat: bool = True, timeout: int = 0,
                 handler: 'Callable[..., None]' = None):
        super().__init__()
        self.__cmdId = cmd_id
        self.__request = message
        self.__isRepeat = is_repeat
        self.__timeout = timeout
        self.__handler = handler

        if is_repeat:
            self.__repeatCount = -1
        else:
            self.__repeatCount = 1

    # 开始监听
    def start(self):
        # 异步发送消息
        asyncio.create_task(self.send(cmd_id=self.__cmdId, message=self.__request))

        # 注册消息监听
        socket.register_msg_handler(cmd=self.__cmdId, handler=self)

        # #test：模拟消息回调
        # asyncio.create_task(self.test())

    # 停止监听
    def stop(self):
        # TODO：移除消息监听
        pass

    # DefaultMsgHandler
    def handle_msg(self, message):
        print('receive msg:', message)
        # 处理监听次数
        if self.__repeatCount > 0:
            # 有监听次数
            self.__handle_msg(message)
            self.__repeatCount -= 1
        elif self.__repeatCount == -1:
            # 无限监听
            self.__handle_msg(message)

    def __handle_msg(self, message):
        if self.__handler is not None:
            self.__handler(self.parse_msg(message))


class ASROfflineApi(BaseEventApi):
    """
    离线asr监听
    持续监听
    """

    async def execute(self):
        pass

    def __init__(self, text: str, handler: 'Callable[..., None]'):
        cmd_id = 54
        request = SpeechRecogniseRequest()
        # request.asrText = text

        super().__init__(cmd_id=cmd_id, message=request, is_repeat=True, handler=handler)

    def parse_msg(self, message):
        print('ASROfflineApi parseMsg:', message)

        if not isinstance(message, Message):
            return None

        data = message.bodyData

        response = SpeechRecogniseResponse()

        response.ParseFromString(data)

        return response


class PlayTTSApi(BaseBlockApi):

    def parse_msg(self, message):
        pass

    def __init__(self, param: map):
        super().__init__()
        self.text = param['text']
        self.type = param['type']

    async def execute(self):
        request = ControlTTSRequest()
        request.text = self.text
        request.type = self.type

        return await self.send(cmd_id=100, message=request, timeout=10)


async def main():
    def hand_asr_offline(msg: SpeechRecogniseResponse):
        print('hand_asr_offline msg:', msg)

    observe_asr_offline = ASROfflineApi('监听离线asr', hand_asr_offline)

    play_tts = PlayTTSApi({'text': 'play_tts', 'type': 1})

    # await observe_asr_offline.start()
    # await play_tts.execute()

    # task1 = asyncio.create_task(observe_asr_offline.start())

    # task2 = asyncio.create_task(play_tts.action())

    result = await play_tts.execute()

    print(result)
    observe_asr_offline.start()

    print('main end')

    while True:
        await asyncio.sleep(30)
        break

    # try:
    #     input("Press enter to exit...\n\n")
    # finally:
    #     exit()

# asyncio.run(main())
