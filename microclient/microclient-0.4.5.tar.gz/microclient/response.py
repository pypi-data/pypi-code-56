from json import JSONDecodeError
from typing import Callable
from loguru import logger

import requests


class LazyResponse:
    """
    WORK IN PROGRESS
    """

    def __init__(self, method_call: Callable[..., requests.Response], url: str, method: str, data=None):
        self._response: requests.Response = None
        self._get_response = method_call
        self.url = url
        self.method = method
        self.request_data = data

    def _load_response(self):
        if not self._response:
            logger.info(f"Calling url {self.url} with method: {self.method} and data: {self.request_data}")
            self._response = self._get_response()
            logger.info(f"{self.url} responded with status code {self.status}")

    @property
    def data(self):
        self._load_response()
        try:
            response_data = self._response.json()
        except JSONDecodeError:
            logger.warning(f"{self.url} did not respond with valid JSON, falling back to raw content (probably HTML).")
            response_data = self._response.content
        return response_data

    @property
    def status(self):
        self._load_response()
        return self._response.status_code

    @property
    def headers(self):
        self._load_response()
        return self._response.headers
