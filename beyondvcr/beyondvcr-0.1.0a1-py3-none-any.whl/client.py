import logging
import requests
from urllib.parse import parse_qsl

logger = logging.getLogger(__name__)


def parse_post_body(body):
    "Parse a POST body into a dictionary of params and values"
    return dict(parse_qsl(body, keep_blank_values=True))


class Client:
    """
    Client for the Mock HTTP Server

    This is used to set up the mock in the tests setup.

    It also has functions to inspect the calls that were made,
    that can be used in the tests assertions.
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self._session = requests.Session()

    def reset(self):
        return self._session.request("MOCK_RESET", self.base_url)

    def mock_request(self, method, path, status_code=200, **kwargs):
        if not method.startswith("MOCK_"):
            raise ValueError("http verb for mock requests should start with mock_")
        headers = kwargs.pop("headers", {})
        headers["MOCK_STATUS"] = str(status_code)
        return self._session.request(
            method, self.base_url + path, headers=headers, **kwargs
        )

    def mock_get(self, path, status_code=200, **kwargs):
        return self.mock_request("MOCK_GET", path, status_code, **kwargs)

    def mock_post(self, path, status_code=200, **kwargs):
        return self.mock_request("MOCK_POST", path, status_code, **kwargs)

    def mock_put(self, path, status_code=200, **kwargs):
        return self.mock_request("MOCK_PUT", path, status_code, **kwargs)

    def mock_delete(self, path, status_code=200, **kwargs):
        return self.mock_request("MOCK_DELETE", path, status_code, **kwargs)

    def fetch_recorded_requests(self):
        return self._session.request("MOCK_RETRIEVE", self.base_url).json()

    def find_recorded_request(self, method, path):
        for req in self.fetch_recorded_requests():
            if method == req["method"] and req["path"] == path:
                return req

    def assert_request_sent(self, method, path):
        # TODO: future improvements: take in consideration body and/or headers
        # (or allow to provide a custom function for matching)
        recorded = {(r["method"], r["path"]) for r in self.fetch_recorded_requests()}
        if (method, path) not in recorded:
            raise AssertionError(
                "Request {} {} not found in recorded requests: {}".format(
                    method, path, recorded
                )
            )
