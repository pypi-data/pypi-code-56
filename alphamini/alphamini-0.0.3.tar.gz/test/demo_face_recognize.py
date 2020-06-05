import asyncio

from blockapi.block_observe import ObserveFaceRecognise
from blockapi.block_sound import PlayTTS
from dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_ObserveFaceRecognise():
    observer: ObserveFaceRecognise = ObserveFaceRecognise()

    def handler(msg):
        print(f"{msg}")
        if msg.isSuccess and msg.faceInfos:
            asyncio.create_task(__tts(msg.faceInfos[0].name))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(name):
    await PlayTTS(text=f'你好， {name}').execute()


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveFaceRecognise())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
