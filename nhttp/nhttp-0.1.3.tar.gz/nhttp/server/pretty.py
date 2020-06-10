from .handler import Handler
from .req_info import Request
from .resp_writer import ResponseWriter


class PrettyFuncHandler(Handler):
    def __init__(self, handle_func):
        self.__handle_func = handle_func

    def serve_http(self, response_writer :ResponseWriter, request :Request):
        iterobj = self.__handle_func(response_writer, request)
        self.__send(iterobj, response_writer)

    def __send(self, iterable, response_writer :ResponseWriter):
        if not hasattr(iterable, '__iter__'):
            return

        if isinstance(iterable, str):
            response_writer.write(iterable)
            return

        elif isinstance(iterable, bytes):
            response_writer.write_bytes(iterable)

        else:
            for p in iterable:
                self.__send(p)
