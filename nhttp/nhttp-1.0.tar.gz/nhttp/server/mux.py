import threading

from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from .resp_writer import ResponseWriter
from .req_info import Request
from .handler import Handler, FuncHandler, RedirectHandler

from ..exceptions import MultipleRegistrationException


__all__ = ['MuxEntry', 'ServerMux']


class MuxEntry:
    def __init__(self, pattern :str, handler :Handler):
        self.pattern = pattern
        self.handler = handler


class ServerMux(BaseHTTPRequestHandler):
    __entry_map = {}
    
    @classmethod
    def set_handle_func(self, pattern :str, handle_func :str):
        h = FuncHandler(handle_func)
        
        self.set_handler(pattern, h)
    
    @classmethod
    def set_handler(self, pattern :str, handler :Handler):
        if pattern in self.__entry_map:
            raise MultipleRegistrationException()

        m = MuxEntry(pattern, handler)

        self.__entry_map[pattern] = m
        
        # redirect to pattern
        if pattern != '/' and pattern[-1] == '/' \
                and pattern[:-1] not in self.__entry_map:
            sp = pattern[:-1]
            
            self.__entry_map[sp] = MuxEntry(
                    sp, RedirectHandler(pattern))
    
    def __find_handler(self, pattern :str) -> Handler:
        pattern, *_ = pattern.split('?')  # Remove query part

        m = self.__entry_map.get(pattern, None)

        if m is None:
            return self.__find_best_match_handler(pattern)

        return m.handler

    def __find_best_match_handler(self, path :str):
        max_length = 0
        target_handler = None

        for k, v in self.__entry_map.items():
            if not self.__is_match(k, path):
                continue

        if max_length < len(k):
            max_length = len(k)
            target_handler = v.handler

        return target_handler

    def __is_match(self, pattern :str, path :str) -> bool:
        if pattern[-1] != '/':
            return pattern == path

        l = len(pattern)

        return path[:l] == pattern and len(path) >= l

    def __do_request(self, method :str):
        handler = self.__find_handler(self.path)

        if handler is None:
            self.send_error(404)
            return

        respw = ResponseWriter(self)
        req = Request(self, method)
        
        # handle_thread = threading.Thread(
        #        target=handler.serve_http, args=(respw, req))
        # handle_thread.setDaemon(True)
        handler.serve_http(respw, req)

    def do_GET(self):
        self.__do_request('GET')

    def do_POST(self):
        self.__do_request('POST')
