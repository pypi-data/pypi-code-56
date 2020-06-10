from .handler_enums import FILE_HANDLER_TYPE

# TODO: Ugly code, need to be refactored
from .drivers.minio_file_driver import MinioFileDriver
from .drivers.local_file_driver import LocalFileDriver
from .drivers.s3_file_driver import S3FileDriver
from .drivers.null_file_driver import NullFileDriver

_handlers = {
        FILE_HANDLER_TYPE.NULL: NullFileDriver,
        FILE_HANDLER_TYPE.LOCAL: LocalFileDriver,
        FILE_HANDLER_TYPE.S3: S3FileDriver,
        FILE_HANDLER_TYPE.MINIO: MinioFileDriver
    }


def get_file_driver(handler_type):
    return _handlers[handler_type]()
