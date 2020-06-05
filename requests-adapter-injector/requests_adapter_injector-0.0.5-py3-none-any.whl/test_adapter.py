import io
import json
import requests

from .logger import logger


class TestAdapter(requests.adapters.BaseAdapter):
    def __init__(self):
        super().__init__()

    def send(
        self,
        request,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None
    ):
        logger.debug(
            "TestAdapter.send %s %s %s %s",
            request.method,
            request.url,
            request.headers,
            request.body,
        )
        response_bytes = json.dumps({
            "method": request.method,
            "url": request.url,
            "headers": dict(request.headers),
            "body": request.body,
        }).encode()
        response = requests.Response()
        response.status_code = 200
        response.headers["content-encoding"] = "application/json"
        response.url = request.url
        response.request = request
        response.headers["Content-Length"] = str(len(response_bytes))
        response.raw = io.BytesIO(response_bytes)
        return response

    def close(self):
        pass
