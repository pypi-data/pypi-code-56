from enum import IntEnum, Enum, unique, auto


@unique
class ServiceHTTPCodes(IntEnum):
    OK = 200
    BAD_REQUEST = 400
    UNPROCESSABLE_ENTITY = 422
    SERVER_ERROR = 500


@unique
class ServiceHTTPMethods(Enum):
    GET = auto()
    POST = auto()
