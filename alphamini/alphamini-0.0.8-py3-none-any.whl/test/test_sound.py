import asyncio

from mini.blockapi import errors
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program

from mini.blockapi.base_api import BlockApiResultType
from mini.blockapi.block_sound import PlayTTS, ControlTTSResponse, TTSControlType
from mini.blockapi.block_sound import PlayAudio, PlayAudioResponse
from mini.blockapi.block_sound import FetchAudioList, GetAudioListResponse, AudioType
from mini.blockapi.block_sound import StopAllAudio, StopAudioResponse
from mini.blockapi.block_sound import PlayOnlineMusic, MusicResponse


async def test_play_tts():
    block: PlayTTS = PlayTTS(text="你好， 我是悟空， 啦啦啦", control_type=TTSControlType.START)
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == BlockApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'


async def test_play_audio():
    block: PlayAudio = PlayAudio(
        url=["http://yun.lnpan.com/music/download/ring/000/075/5653bae83917a892589b372782175dd8.amr"])
    (resultType, response) = await block.execute()

    print(f'test_play_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == BlockApiResultType.Success, 'test_play_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_audio result unavailable'
    assert response.isSuccess, 'test_play_audio failed'


async def test_get_audio_list():
    block: FetchAudioList = FetchAudioList(audio_type=AudioType.INNER)
    (resultType, response) = await block.execute()

    print(f'test_get_audio_list result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_get_audio_list timetout'
    assert response is not None and isinstance(response, GetAudioListResponse), 'test_play_audio result unavailable'
    assert response.isSuccess, 'test_get_audio_list failed'


async def test_stop_audio():
    block: PlayTTS = PlayTTS(is_serial=False, text="你让我说，让我说，不要打断我，不要打断我，不要打断我")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(2)
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    assert resultType == BlockApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'


async def test_play_online_music():
    block: PlayOnlineMusic = PlayOnlineMusic(name='我的世界')
    (resultType, response) = await block.execute()

    print(f'test_play_online_music result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_play_online_music timetout'
    assert response is not None and isinstance(response, MusicResponse), 'test_play_online_music result unavailable'
    assert response.isSuccess, 'test_play_online_music failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_tts())
        asyncio.get_event_loop().run_until_complete(test_get_audio_list())
        asyncio.get_event_loop().run_until_complete(test_stop_audio())
        asyncio.get_event_loop().run_until_complete(test_play_online_music())
        asyncio.get_event_loop().run_until_complete(test_play_audio())
        asyncio.get_event_loop().run_until_complete(shutdown())
