from .handler import FileServerHandler
from . import *


set_handler('/', FileServerHandler('/', '.'))

listen_and_service(':5013')
