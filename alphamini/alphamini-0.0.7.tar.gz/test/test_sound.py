import asyncio

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from blockapi.block_sound import PlayTTS, PlayAudio, FetchAudioList, StopAllAudio
from dns.dns_browser import WiFiDevice
from test.test_connect import test_get_device_by_name, test_start_run_program
from test.test_connect import test_connect, shutdown


async def test_play_tts():
    block: PlayTTS = PlayTTS(text="你好， 我是悟空， 啦啦啦")
    response = await block.execute()
    print(f'tes_play_tts: {response}')


async def test_play_audio():
    block: PlayAudio = PlayAudio(
        url="http://yun.lnpan.com/music/download/ring/000/075/5653bae83917a892589b372782175dd8.amr")
    response = await block.execute()
    print(f'test_play_audio: {response}')


async def test_get_audio_list():
    block: FetchAudioList = FetchAudioList()
    response = await block.execute()
    print(f'test_get_audio_list: {response}')


async def test_stop_audio():
    block: PlayTTS = PlayTTS(is_serial=False, text="你让我说，让我说，不要打断我，不要打断我，不要打断我")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(2)
    block: StopAllAudio = StopAllAudio()
    response = await block.execute()
    print(f'test_stop_audio.stop_all_audio:{response}')


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_tts())
        asyncio.get_event_loop().run_until_complete(test_play_audio())
        asyncio.get_event_loop().run_until_complete(test_get_audio_list())
        asyncio.get_event_loop().run_until_complete(test_stop_audio())
        asyncio.get_event_loop().run_until_complete(shutdown())
