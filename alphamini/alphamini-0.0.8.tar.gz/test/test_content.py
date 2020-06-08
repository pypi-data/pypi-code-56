import asyncio

from mini.dns.dns_browser import WiFiDevice
from mini.pb2.cloudtranslate_pb2 import CN, EN
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name

from mini.blockapi.base_api import BlockApiResultType
from mini.blockapi.block_content import QueryWiKi, WikiResponse
from mini.blockapi.block_content import StartTranslate, TranslateResponse


async def test_query_wiki():
    block: QueryWiKi = QueryWiKi(query='优必选')
    (resultType, response) = await block.execute()

    print(f'test_query_wiki result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_query_wiki timetout'
    assert response is not None and isinstance(response, WikiResponse), 'test_query_wiki result unavailable'
    assert response.isSuccess, 'query_wiki failed'


async def test_start_translate():
    block: StartTranslate = StartTranslate(query="张学友", from_lan=CN, to_lan=EN)
    (resultType, response) = await block.execute()

    print(f'test_start_translate result: {response}')

    assert resultType == BlockApiResultType.Success, 'test_start_translate timetout'
    assert response is not None and isinstance(response, TranslateResponse), 'test_start_translate result unavailable'
    assert response.isSuccess, 'start_translate failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_query_wiki())
        asyncio.get_event_loop().run_until_complete(test_start_translate())
        asyncio.get_event_loop().run_until_complete(shutdown())
