import asyncio

from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name

from mini.blockapi.base_api import BlockApiResultType
from mini.blockapi.block_sence import FaceDetect, FaceDetectResponse
from mini.blockapi.block_sence import FaceAnalysis, FaceAnalyzeResponse
from mini.blockapi.block_sence import ObjectRecognise, RecogniseObjectResponse, ObjectRecogniseType
from mini.blockapi.block_sence import FaceRecognise, FaceRecogniseResponse
from mini.blockapi.block_sence import TakePicture, TakePictureResponse, TakePictureType
from mini.blockapi.block_sence import GetInfraredDistance, GetInfraredDistanceResponse
from mini.blockapi.block_sence import GetRegisterFaces, GetRegisterFacesResponse


async def test_face_detect():
    block: FaceDetect = FaceDetect(timeout=10)
    (resultType, response) = await block.execute()

    print(f'test_face_detect result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_face_detect timetout'
    assert response is not None and isinstance(response, FaceDetectResponse), 'test_face_detect result unavailable'
    assert response.isSuccess, 'face_detect failed'


async def test_face_analysis():
    block: FaceAnalysis = FaceAnalysis(timeout=10)
    (resultType, response) = await block.execute()

    print(f'test_face_analysis result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_face_analysis timetout'
    assert response is not None and isinstance(response, FaceAnalyzeResponse), 'test_face_analysis result unavailable'
    assert response.isSuccess, 'face_analysis failed'


async def test_object_Recognise():
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FLOWER, timeout=10)
    (resultType, response) = await block.execute()

    print(f'test_object_Recognise result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_object_Recognise timetout'
    assert response is not None and isinstance(response,
                                               RecogniseObjectResponse), 'test_object_Recognise result unavailable'
    assert response.isSuccess, 'test_object_Recognise failed'


async def test_take_picture():
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.IMMEDIATELY).execute()

    print(f'test_take_picture result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_take_picture timetout'
    assert response is not None and isinstance(response, TakePictureResponse), 'test_take_picture result unavailable'
    assert response.isSuccess, 'test_take_picture failed'


async def test_face_recognise():
    (resultType, response) = await FaceRecognise(timeout=10).execute()

    print(f'test_face_recognise result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_face_recognise timetout'
    assert response is not None and isinstance(response,
                                               FaceRecogniseResponse), 'test_face_recognise result unavailable'
    assert response.isSuccess, 'test_face_recognise failed'


async def test_get_infrared_distance():
    (resultType, response) = await GetInfraredDistance().execute()

    print(f'test_get_infrared_distance result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_get_infrared_distance timetout'
    assert response is not None and isinstance(response,
                                               GetInfraredDistanceResponse), 'test_get_infrared_distance result unavailable'
    assert response.distance > 0, 'test_get_infrared_distance failed'


async def test_get_register_faces():
    (resultType, response) = await GetRegisterFaces().execute()

    print(f'test_get_register_faces result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_get_register_faces timetout'
    assert response is not None and isinstance(response,
                                               GetRegisterFacesResponse), 'test_get_register_faces result unavailable'
    assert response.isSuccess, 'test_get_register_faces failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_face_detect())
        asyncio.get_event_loop().run_until_complete(test_face_analysis())
        asyncio.get_event_loop().run_until_complete(test_take_picture())
        asyncio.get_event_loop().run_until_complete(test_face_recognise())
        asyncio.get_event_loop().run_until_complete(test_get_infrared_distance())
        asyncio.get_event_loop().run_until_complete(test_get_register_faces())
        asyncio.get_event_loop().run_until_complete(shutdown())
