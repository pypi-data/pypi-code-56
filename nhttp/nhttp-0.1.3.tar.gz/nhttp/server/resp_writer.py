from http.server import BaseHTTPRequestHandler
from .headers import NORMAL_HTTP_HEADERS


__all__ = ['ResponseWriter']


class ResponseWriter:
    def __init__(self, handler :BaseHTTPRequestHandler):
        self.__base_handler = handler
        self.__base_headers = NORMAL_HTTP_HEADERS

    @property
    def resp_file(self):
        return self.__base_handler.wfile

    @property
    def _base_handler(self):
        return self.__base_handler

    @property
    def base_headers(self) -> dict:
        return self.__headers

    def send_respone(self, code :int):
        """
        (Attention!) This method is not use any more!
        (Attention!) Use send_response instead.
        """

        self.__base_handler.send_response(code)

    def send_response(self, code :int):
        self.__base_handler.send_response(code)

    def send_header(self, kw_dict :dict):
        h = self.__base_headers.copy()
        h.update(kw_dict)

        for k, v in h.items():
            self.__base_handler.send_header(k, v)

        self.__base_handler.end_headers()

    def send_error(self, code :int, message :str=''):
        self.__base_handler.send_error(code, message)

    def write(self, text :str, encoding='UTF-8'):
        self.__base_handler.wfile.write(text.encode(encoding))

    def write_bytes(self, b :bytes):
        self.__base_handler.wfile.write(b)
