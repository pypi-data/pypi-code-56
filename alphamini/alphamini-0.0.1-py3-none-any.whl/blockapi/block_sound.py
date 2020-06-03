#!/usr/bin/env python3

from blockapi.base_api import BaseBlockApi, DEFAULT_TIMEOUT
from blockapi.cmdid import PCProgramCmdId
from pb2 import cloudstorageurls_pb2
from pb2.pccodemao_message_pb2 import Message

from pb2.codemao_controltts_pb2 import ControlTTSRequest, ControlTTSResponse
from pb2.codemao_playaudio_pb2 import PlayAudioRequest, PlayAudioResponse
from pb2.codemao_stopaudio_pb2 import StopAudioRequest, StopAudioResponse
from pb2.codemao_getaudiolist_pb2 import GetAudioListRequest, GetAudioListResponse


class PlayTTS(BaseBlockApi):
    """
    播放TTS
    type: 1 播放 0 停止播放
    """

    def __init__(self, is_serial: bool = True, text: str = None, _type: int = 1):
        assert text is not None, 'tts text could not be None'
        self.__isSerial = is_serial
        self.__text = text
        self.__type = _type

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = ControlTTSRequest()
        request.text = self.__text
        request.type = self.__type

        cmd_id = PCProgramCmdId.PLAY_TTS_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlTTSResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayAudio(BaseBlockApi):
    """
    播放音效
    默认音效存储类型为阿里私有云
    """

    def __init__(self, is_serial: bool = True, url: str = None, volume: float = 0):
        assert url is not None, 'str could not be None'
        self.__isSerial = is_serial
        self.__url = url
        self.__volume = volume
        self.__cloudStorageType = cloudstorageurls_pb2.ALIYUN_PRIVATE

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        cloud = cloudstorageurls_pb2.CloudStorage()
        cloud.type = self.__cloudStorageType
        cloud.url = self.__url

        request = PlayAudioRequest()

        request.cloud = cloud
        request.volume = self.__volume

        cmd_id = PCProgramCmdId.PLAY_AUDIO_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAudio(BaseBlockApi):
    """
    停止所有音效
    """

    def __init__(self, is_serial: bool = True, ):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = StopAudioRequest()

        cmd_id = PCProgramCmdId.STOP_AUDIO_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = StopAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FetchAudioList(BaseBlockApi):
    """
    获取机器人的音效列表
    """

    def __init__(self, is_serial: bool = True, search_type: int = 0):
        self.__isSerial = is_serial
        self.__searchType = search_type

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = GetAudioListRequest()

        request.searchType = self.__searchType

        cmd_id = PCProgramCmdId.GET_AUDIO_LIST_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetAudioListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
