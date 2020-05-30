from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from .simple_types import base64Binary


class Compression(Enum):
    BZIP2 = "bzip2"
    NONE = "none"
    ZLIB = "zlib"


_no_default = object()


@dataclass
class BinData(base64Binary):
    big_endian: bool = _no_default  # type: ignore
    length: int = _no_default  # type: ignore
    compression: Optional[Compression] = Compression("none")

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.length is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'length'")
        if self.big_endian is _no_default:
            raise TypeError(
                "__init__ missing 1 required argument: 'big_endian'"
            )
