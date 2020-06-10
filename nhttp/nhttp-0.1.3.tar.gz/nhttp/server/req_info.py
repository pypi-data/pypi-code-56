from urllib.parse import unquote
from typing import Tuple

from http.server import BaseHTTPRequestHandler


__all__ = ['Request']


class Request:
    def __init__(self, handler :BaseHTTPRequestHandler, method :str):
        self.__base_handler = handler
        self.__method = method

        self.__content = {}
        self.__content_type = ''
        self.__content_charset = 'UTF-8'
        self.__raw_content = b''

        # self.read_content()

        self.__url, self.__query = self.__parse_url(
                self.__base_handler.path)

        self.__content_length = 0

    @property
    def content(self):
        return self.__content

    @property
    def client_address(self):
        return self.__base_handler.client_address

    @property
    def method(self):
        return self.__method

    @property
    def url(self):
        return self.__url

    @property
    def query_dict(self) -> dict:
        return self.__query

    @property
    def headers(self):
        return self.__base_handler.headers

    @property
    def request_file(self):
        return self.__base_handler.rfile

    @property
    def raw_content(self) -> bytes:
        return self.__raw_content

    @property
    def path(self) -> str:
        return self.__base_handler.path

    @property
    def content_length(self) -> int:
        return self.content_length

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def _base_handler(self):
        return self.__base_handler

    def __parse_url(self, url_str :str):
        url_str = unquote(url_str)
        url, *query_str = url_str.split('?', 1)
        
        if len(query_str) == 0:
            return url, {}

        query_str = query_str[0]

        if '=' not in query_str:
            return url, {}

        # parse query
        qd = {}

        for eq in query_str.split('&'):
            if '=' not in eq:
                continue

            k, v = eq.split('=', 1)
            qd[unquote(k)] = unquote(v)

        return unquote(url), qd

    def get_header(self, key :str, fail_obj=None):
        for k, v in self.__base_handler.headers.items():
            if k.lower() == key.lower():
                return v
        return fail_obj

    def __parse_content_type(self, typestr :str):
        """
        :return (real_type, main_type, sub_type, params)
        """

    def __read_content_info(self):
        ctl = self.get_header('content-length', 0)
        ctt = self.get_header('content-type', '')

        self.__content_length = ctl
        self.__content_type = ctt

    def read_content(self, size=-1):
        if self.__raw_content:
            return

        try:
            length = self.get_header('content-length')

            if length is None:
                return

            length = int(length)

            if -1 < size < length:
                pass

            chset = self.headers.get_charset()
            cont_type = self.headers.get_content_type()

            if chset is not None:
                self.__content_charset = chset

            if cont_type is not None:
                self.__content_type = cont_type

            self.__raw_content = self.__base_handler.rfile.read(length)

        except (KeyError, TypeError):
            # TODO log.
            raise
