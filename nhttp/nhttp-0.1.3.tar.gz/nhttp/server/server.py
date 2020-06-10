import sys
import traceback

from socketserver import ThreadingMixIn
from http.server import HTTPServer
from .._internal import color


__all__ = ['NHTTPThreadingHTTPServer']


# old version of python do not have 'ThreadingHTTPServer'
class NHTTPThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

    def serve_forever(self):
        print(color.color('Serve HTTP at ( %s : %s )' % 
            self.server_address, color.COLOR_TX_GREEN))

        try:
            super().serve_forever()
        except KeyboardInterrupt:
            print('\rKeyboard interrupt')

    def handle_error(self, requests :bytes, client_address :tuple):
        exc_str = traceback.format_exc()

        sys.stderr.write('%s\n%s\n%s\n' % 
                         (
                             color.color('------ [!] An exception raised ------', 
                                 color.COLOR_TX_YELLOW),
                             color.color(exc_str, color.COLOR_TX_RED),
                             color.color('-' * 36, color.COLOR_TX_YELLOW),
                         ))
