#  Drakkar-Software OctoBot-Backtesting
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import asyncio
import json
from os.path import join, isdir
from os import makedirs

from aiohttp import ClientSession, ClientPayloadError

from octobot_backtesting.enums import DataFormats
from octobot_commons.logging.logging_util import get_logger

from octobot_backtesting.constants import BACKTESTING_FILE_PATH
from octobot_backtesting.data.database import DataBase
from octobot_backtesting.data.data_file_manager import get_backtesting_file_name
from octobot_backtesting.importers.data_importer import DataImporter


class DataCollector:
    IMPORTER = DataImporter

    def __init__(self, config, path=BACKTESTING_FILE_PATH, data_format=DataFormats.REGULAR_COLLECTOR_DATA):
        self.config = config
        self.path = path
        self.logger = get_logger(self.__class__.__name__)

        self.should_stop = False
        self.file_name = get_backtesting_file_name(self.__class__, data_format)

        self.database = None
        self.aiohttp_session = None
        self.file_path = None
        self._ensure_file_path()
        self.set_file_path()

    async def initialize(self) -> None:
        pass

    async def stop(self) -> None:
        self.should_stop = True

    async def start(self) -> None:
        raise NotImplementedError("Start is not implemented")

    def _ensure_file_path(self):
        if not isdir(self.path):
            makedirs(self.path)

    def set_file_path(self) -> None:
        self.file_path = join(self.path, self.file_name) if self.path else self.file_name

    def create_database(self) -> None:
        if not self.database:
            self.database = DataBase(self.file_path)

    def create_aiohttp_session(self) -> None:
        if not self.aiohttp_session:
            self.aiohttp_session = ClientSession()

    async def stop_aiohttp_session(self) -> None:
        if self.aiohttp_session:
            await self.aiohttp_session.close()

    async def execute_request(self, url, params=None, headers=None):
        response = await self.aiohttp_session.get(url, params=params, headers=headers)
        if response.status != 200:
            if response.status == 502:  # bad gateway (should retry)
                self.logger.warning("Got a bad gateway error, retrying...")
                await asyncio.sleep(60)
                return await self.execute_request(url, params=params, headers=headers)
            else:
                try:
                    message = json.loads(await response.text())['message']
                except json.JSONDecodeError:
                    message = await response.text()
                self.logger.error(f"Error when requesting url {url} / "
                                  f"message : {message} / "
                                  f"code : {response.status} / "
                                  f"reason : {response.reason}")
            return None
        try:
            return json.loads(await response.text())
        except ClientPayloadError as e:
            self.logger.error(f"Failed to extract payload text : {e}")
            return None

    async def fetch_with_continuation(self, continuation_url_key, json_answer, headers, callback):
        if continuation_url_key in json_answer:
            answer = await self.execute_request(json_answer[continuation_url_key], headers=headers)
            if answer is None:
                return

            await callback(answer["data"])

            await self.fetch_with_continuation(continuation_url_key, answer, headers, callback)
