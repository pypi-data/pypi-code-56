#!/usr/bin/env python3
import abc
import asyncio
import enum
from abc import ABC
from typing import Callable, Union

from ..channels.websocket_client import ubt_websocket as _UBTWebSocket, AbstractMsgHandler

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

    async def send(self, cmd_id: int, message, timeout: int) -> Union[object, bool]:

        assert cmd_id >= 0, 'cmdId should not be negative number in BaseBlockApi'
        assert message is not None, 'message should not be none in BaseBlockApi'
        # 通用的发送消息逻辑
        if timeout <= 0:
            return await socket.send_msg0(cmd_id, message)
        else:
            result = await socket.send_msg(cmd_id, message, timeout)
            if result:
                return BlockApiResultType.Success, self.parse_msg(result)
            else:
                return BlockApiResultType.Timeout, None

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


class BaseEventApi(BaseBlockApiNoNeedResponse, AbstractMsgHandler, ABC):
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

    def set_handler(self, handler: 'Callable[..., None]' = None):
        self.__handler = handler

    # 开始监听
    def start(self):
        # 发送消息
        # asyncio.run(self.send(cmd_id=self.__cmdId, message=self.__request))
        asyncio.create_task(self.send(cmd_id=self.__cmdId, message=self.__request))
        # 注册监听
        socket.register_msg_handler(cmd=self.__cmdId, handler=self)

    # 停止监听
    def stop(self):
        # 移除消息监听
        socket.unregister_msg_handler(cmd=self.__cmdId, handler=self)

    # AbstractMsgHandler
    def handle_msg(self, message):
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
