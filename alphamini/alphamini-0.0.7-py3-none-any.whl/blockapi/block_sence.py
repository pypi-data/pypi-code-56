#!/usr/bin/env python3

from ..blockapi.base_api import BaseBlockApi, DEFAULT_TIMEOUT
from ..blockapi.cmdid import PCProgramCmdId
from ..pb2.codemao_faceanalyze_pb2 import FaceAnalyzeRequest, FaceAnalyzeResponse
from ..pb2.codemao_facedetect_pb2 import FaceDetectResponse
from ..pb2.codemao_facerecognise_pb2 import FaceRecogniseRequest, FaceRecogniseResponse
from ..pb2.codemao_getinfrareddistance_pb2 import GetInfraredDistanceRequest, GetInfraredDistanceResponse
from ..pb2.codemao_getregisterfaces_pb2 import GetRegisterFacesRequest, GetRegisterFacesResponse
from ..pb2.codemao_recogniseobject_pb2 import RecogniseObjectRequest, RecogniseObjectResponse
from ..pb2.codemao_takepicture_pb2 import TakePictureRequest, TakePictureResponse
from ..pb2.pccodemao_message_pb2 import Message


class FaceDetect(BaseBlockApi):
    """
    人脸检测（个数）
    """

    def __init__(self, is_serial: bool = True, timeout: int = 0):
        assert timeout > 0, 'FaceDetect timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = FaceDetect()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_DETECT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceAnalysis(BaseBlockApi):
    """
    人脸分析（性别）
    """

    def __init__(self, is_serial: bool = True, timeout: int = 0):
        assert timeout > 0, 'FaceAnalysis timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = FaceAnalyzeRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_ANALYSIS_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceAnalyzeResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ObjectRecognise(BaseBlockApi):
    """
    物体识别
    1(水果)  2（手势） 3（花)
    """

    def __init__(self, is_serial: bool = True, object_type: int = None, timeout: int = 0):
        assert timeout > 0, 'ObjectRecognise timeout should be positive'
        assert object_type is not None and object_type > 0, 'objectType should not be None,and should be positive'
        self.__isSerial = is_serial
        self.__objectType = object_type
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = RecogniseObjectRequest()
        request.objectType = self.__objectType
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.RECOGNISE_OBJECT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = RecogniseObjectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceRecognise(BaseBlockApi):
    """
    人脸识别
    """

    def __init__(self, is_serial: bool = True, timeout: int = 0):
        assert timeout > 0, 'ObjectRecognise timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = FaceRecogniseRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_RECOGNISE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class TakePicture(BaseBlockApi):
    """
    拍照
    """

    def __init__(self, is_serial: bool = True, ptype: int = 0):
        assert ptype > 0, 'ObjectRecognise timeout should be positive'
        self.__isSerial = is_serial
        self.__type = ptype

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = TakePictureRequest()
        request.type = self.__type

        cmd_id = PCProgramCmdId.TAKE_PICTURE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = TakePictureResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetInfraredDistance(BaseBlockApi):
    """
    获取红外距离
    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = GetInfraredDistanceRequest()

        cmd_id = PCProgramCmdId.GET_INFRARED_DISTANCE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetRegisterFaces(BaseBlockApi):
    """
    获取已注册的人脸列表
    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = GetRegisterFacesRequest()

        cmd_id = PCProgramCmdId.GET_REGISTER_FACES_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetRegisterFacesResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
