import aiohttp
import logging

_client_session = None


class CommError(Exception):
    pass


async def http_get_json(url, headers={}):
    return await _http_request_json(url, 'GET', None, headers)


async def http_post_json(url, payload={}, headers={}):
    return await _http_request_json(url, 'POST', payload, headers)


async def http_get_raw(url, headers={}):
    global _client_session
    if _client_session is None:
        _client_session = aiohttp.ClientSession()
    session = _client_session
    async with session.get(url, ssl=False, headers=headers) as r:
        if not (r.status >= 200 and r.status < 300):
            raise CommError(f'{url} {method} returns {r.status}')
        return await r.read()


async def _http_request_json(url, method, payload, headers={}):
    global _client_session
    if _client_session is None:
        _client_session = aiohttp.ClientSession()
    session = _client_session
    if method == 'GET':
        async with session.get(url, ssl=False, headers=headers) as r:
            # print(r.status,r.json())
            if not (r.status >= 200 and r.status < 300):
                logging.error(await r.json())
                raise CommError(f'{url} {method} returns {r.status}')
            return await r.json()
    elif method == 'POST':
        async with session.post(url, ssl=False, json=payload, headers=headers) as r:
            # print(r.status,r.json())
            if not (r.status >= 200 and r.status < 300):
                logging.error(await r.json())
                raise CommError(f'{url} {method} returns {r.status}')
            return await r.json()
    elif method == 'PATCH':
        async with session.patch(url, ssl=False, json=payload, headers=headers) as r:
            # print(r.status,r.json())
            if not (r.status >= 200 and r.status < 300):
                logging.error(await r.json())
                raise CommError(f'{url} {method} returns {r.status}')
            return await r.json()
    elif method == 'PUT':
        async with session.put(url, ssl=False, json=payload, headers=headers) as r:
            # print(r.status,r.json())
            if not (r.status >= 200 and r.status < 300):
                logging.error(await r.json())
                raise CommError(f'{url} {method} returns {r.status}')
            return await r.json()
    elif method == 'DELETE':
        async with session.delete(url, ssl=False, headers=headers) as r:
            if not (r.status >= 200 and r.status < 300):
                logging.error(await r.json())
                raise CommError(f'{url} {method} returns {r.status}')
            return await r.json()
