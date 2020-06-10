
from .server import NHTTPThreadingHTTPServer
from .mux import ServerMux, MuxEntry
from .resp_writer import ResponseWriter
from .req_info import Request
from .handler import Handler

__mux = ServerMux
__http_server = None


def set_handle_func(pattern :str, handler_func):
    __mux.set_handle_func(pattern, handler_func)


def set_handler(pattern :str, handler :Handler):
    __mux.set_handler(pattern, handler)


def handle(pattern :str):
    """
    Used as a descriptor.
    """

    def wrapper(func):
        set_handle_func(pattern, func)
        return func
    return wrapper


def listen_and_service(address :str):
    try:
        ip, port = address.split(':', 1)

        addr = (ip, int(port))

    except ValueError:
        raise ValueError('Invalid address: \'%s\'')
    
    __http_server = NHTTPThreadingHTTPServer(addr, __mux)

    print('Serve HTTP at (%s : %s)' % addr)
    
    try:
        __http_server.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt')


__all__ = [
            'listen_and_service',
            'handle',
            'set_handler',
            'set_handle_func',

            'ResponseWriter',
            'Request',
          ]
