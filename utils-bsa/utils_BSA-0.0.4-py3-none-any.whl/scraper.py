import os
import json
import aiohttp
import asyncio
import aiofiles

concurrent_requests = 15

async def get_station(stations, monitors_filename, base_url, headers):
    endpoint = "monitors"
    url = os.path.join(base_url, endpoint)
    print('Getting all stations...')
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            data_2 = await resp.text()
        async with aiofiles.open(monitors_filename, 'w') as file:
            await file.write(data_2)
    stations.extend([item['slug'] for item in data])


async def get_data(station_name, data_folder, base_url, headers):
    endpoint = os.path.join('measurements', station_name)
    params = {'duration': '1d'}
    url = os.path.join(base_url, endpoint)
    print(f'Getting station {station_name}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status == 200:
                data = await resp.text()
                async with aiofiles.open("{}.json".format(os.path.join(data_folder, station_name)), 'w') as file:
                    await file.write(data)
