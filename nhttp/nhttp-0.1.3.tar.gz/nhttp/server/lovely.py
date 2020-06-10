from typing import Iterable

from nhttp.server.handler import Handler
from nhttp.server.req_info import Request
from nhttp.server.resp_writer import ResponseWriter


DEFAULT_HEADERS = {'Content-Type': 'text/html'}


class Response:
    def __init__(self, status_code=200, headers=None, 
                 content_iter :Iterable=None):
        self.__status_code = status_code
        self.__headers = headers \
                if isinstance(headers, dict) else DEFAULT_HEADERS.copy()
        self.__content_iter = content_iter \
                if self.__check_iterable(content_iter) else tuple()

    @property
    def status_code(self) -> int:
        return self.__status_code

    @status_code.setter
    def set_status_code(self, value :int):
        if not isinstance(value, int):
            raise TypeError('HTTP Status Code must be an integer')
        self.__status_code = value

    @property
    def headers(self) -> dict:
        return self.__headers

    @headers.setter
    def set_headers(self, headers :dict):
        if not isinstance(headers, dict):
            raise TypeError('Headers must be a dict')
        self.__headers = headers

    @property
    def content_iter(self) -> Iterable:
        return self.__content_iter

    @content_iter.setter
    def set_content_iter(self, iter :Iterable):
        if not self.__check_iterable(iter):
            raise TypeError('Content iter must be a iterable object')
        self.__content_iter = iter

    def __check_iterable(self, o) -> bool:
        return hasattr(o, '__iter__')


class LovelyFuncHandler(Handler):
    def __init__(self, handle_func):
        self.__handle_func = handle_func

    def serve_http(self, response_writer: ResponseWriter, request: Request):
        resp :Response = self.__handle_func(request)  # request only!

        if not isinstance(resp, Response):
            raise TypeError('handler must return a Response object')

        response_writer.send_response(resp.status_code)
        response_writer.send_header(resp.headers)
        self.__send_content(resp.content_iter, response_writer)

    def __send_content(self, content_iter :Iterable, resp_writer :ResponseWriter):
        if isinstance(content_iter, str):
            resp_writer.write(content_iter)

        elif isinstance(content_iter, bytes):
            resp_writer.write_bytes(content_iter)

        else:
            if not hasattr(content_iter, '__iter__'):
                return

            for e in content_iter:
                self.__send_content(e, resp_writer)


__all__ = ['LovelyFuncHandler', 'Response', 'DEFAULT_HEADERS']
