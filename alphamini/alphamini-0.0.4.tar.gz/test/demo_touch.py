import asyncio

from blockapi.block_expression import ControlBehavior
from blockapi.block_observe import ObserveHeadRacket
from dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_ObserveHeadRacket():
    observer: ObserveHeadRacket = ObserveHeadRacket()

    def handler(msg):
        print("{0}".format(str(msg.type)))
        asyncio.run(__dance())

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __dance():
    await ControlBehavior(name="dance_0002").execute()


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveHeadRacket())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
