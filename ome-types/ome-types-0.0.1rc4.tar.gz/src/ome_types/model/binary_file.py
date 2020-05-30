from typing import Optional

from pydantic.dataclasses import dataclass

from .bin_data import BinData
from .external import External
from .simple_types import NonNegativeLong


@dataclass
class BinaryFile:
    file_name: str
    size: NonNegativeLong
    bin_data: Optional[BinData] = None
    external: Optional[External] = None
    mime_type: Optional[str] = None
