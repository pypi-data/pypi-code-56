import socketserver
import selectors

from .server import NHTTPThreadingHTTPServer
from .mux import ServerMux, MuxEntry
from .resp_writer import ResponseWriter
from .req_info import Request
from .handler import Handler
from .pretty import PrettyFuncHandler


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


def pretty_handle(pattern :str):
    """
    Used as a descriptor
    """

    def wrapper(func):
        set_handler(pattern, PrettyFuncHandler(func))
        return func
    return wrapper


def listen_and_service(address :str, use_epoll=False):
    """Listen and service requests.

    parse request and call handler to deal with.

    :param use_epoll    use selectors.EpollSelector instead of 
                        default socketserver._ServerSelector
                        (PollSelector or SelectSelector).
                        Available only in a environment supporting 
                        epoll like Linux.
    
    (Attention!) use epoll selector may cause unpredictable exception.
                 it just a experimental features, and it is unstable.

    """

    if use_epoll and hasattr(selectors, 'EpollSelector'):
        socketserver._ServerSelector = selectors.EpollSelector

    try:
        ip, port = address.split(':', 1)

        addr = (ip, int(port))

    except ValueError:
        raise ValueError('Invalid address: \'%s\'')
    
    __http_server = NHTTPThreadingHTTPServer(addr, __mux)

    __http_server.serve_forever()


__all__ = [
            'listen_and_service',
            'handle',
            'pretty_handle',
            'set_handler',
            'set_handle_func',

            'ResponseWriter',
            'Request',
          ]
