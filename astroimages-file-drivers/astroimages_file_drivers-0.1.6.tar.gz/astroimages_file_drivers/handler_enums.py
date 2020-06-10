from enum import Enum


class FILE_HANDLER_TYPE(Enum):
    NULL = 0
    LOCAL = 1
    S3 = 2
    MINIO = 3
