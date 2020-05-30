from .client import Redis, StrictRedis
from .connection import (
    BlockingConnectionPool,
    ConnectionPool,
    Connection,
    SSLConnection,
    UnixDomainSocketConnection
)
from .utils import from_url
from .exceptions import (
    AuthenticationError,
    BusyLoadingError,
    ConnectionError,
    DataError,
    InvalidResponse,
    PubSubError,
    ReadOnlyError,
    RedisError,
    ResponseError,
    TimeoutError,
    WatchError
)


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


__version__ = '3.3.8'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = [
    'Redis', 'StrictRedis', 'ConnectionPool', 'BlockingConnectionPool',
    'Connection', 'SSLConnection', 'UnixDomainSocketConnection', 'from_url',
    'AuthenticationError', 'BusyLoadingError', 'ConnectionError', 'DataError',
    'InvalidResponse', 'PubSubError', 'ReadOnlyError', 'RedisError',
    'ResponseError', 'TimeoutError', 'WatchError'
]
