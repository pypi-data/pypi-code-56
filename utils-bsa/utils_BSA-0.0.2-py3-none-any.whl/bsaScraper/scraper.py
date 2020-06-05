import os
from secrets import *
import aiohttp
import asyncio
import aiofiles


concurrent_requests = 15
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
    'auth': get_auth_key(),
    'device': 'api',
}


async def get_station(stations, monitors_filename, base_url):
    endpoint = "monitors"
    url = os.path.join(base_url, endpoint)
    print('Getting all stations...')
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            data = await resp.json()
            data_2 = await resp.text()
        async with aiofiles.open(monitors_filename, 'w') as file:
            await file.write(data_2)
    stations.extend([item['slug'] for item in data])


async def get_data(station_name, data_folder, base_url):
    endpoint = os.path.join('measurements', station_name)
    params = {'duration': '1d'}
    url = os.path.join(base_url, endpoint)
    print(f'Getting station {station_name}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as resp:
            if resp.status == 200:
                data = await resp.text()
                async with aiofiles.open("{}.json".format(os.path.join(data_folder, station_name)), 'w') as file:
                    await file.write(data)
