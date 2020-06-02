import logging
from tornado.ioloop import IOLoop
import tornado.web
from .handlers import *


class Server:

    # Production-ready configuration solution :)
    host = "localhost"
    port = 8888
    logger = None

    def __loggers(self):
        self.logger = logging.getLogger('spacetornado')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s'))
        self.logger.addHandler(handler)
        tornadoLogger = logging.getLogger("tornado.access")
        tornadoLogger.propagate = False
        tornadoLogger.setLevel(logging.DEBUG)
        tornadoLogger.handlers = [handler]

    @staticmethod
    def __app():
        return tornado.web.Application([
            (r"/tokens", Tokens),
            (r"/noun_chunks", NounChunks),
            (r"/entities", Entities),
            (r"/similarity", Similarity)])

    def run(self):
        self.__loggers()
        self.__app().listen(self.port)
        IOLoop.current().start()
