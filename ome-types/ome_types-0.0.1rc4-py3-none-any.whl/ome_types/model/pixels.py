from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .bin_data import BinData
from .channel import Channel
from .plane import Plane
from .simple_types import (
    PixelsID,
    PixelType,
    PositiveFloat,
    PositiveInt,
    UnitsLength,
    UnitsTime,
)
from .tiff_data import TiffData


class DimensionOrder(Enum):
    XYCTZ = "XYCTZ"
    XYCZT = "XYCZT"
    XYTCZ = "XYTCZ"
    XYTZC = "XYTZC"
    XYZCT = "XYZCT"
    XYZTC = "XYZTC"


@dataclass
class Pixels:
    dimension_order: DimensionOrder
    id: PixelsID
    size_c: PositiveInt
    size_t: PositiveInt
    size_x: PositiveInt
    size_y: PositiveInt
    size_z: PositiveInt
    type: PixelType
    big_endian: Optional[bool] = None
    bin_data: List[BinData] = field(default_factory=list)
    channel: List[Channel] = field(default_factory=list)
    interleaved: Optional[bool] = None
    metadata_only: bool = False
    physical_size_x: Optional[PositiveFloat] = None
    physical_size_x_unit: Optional[UnitsLength] = UnitsLength("µm")
    physical_size_y: Optional[PositiveFloat] = None
    physical_size_y_unit: Optional[UnitsLength] = UnitsLength("µm")
    physical_size_z: Optional[PositiveFloat] = None
    physical_size_z_unit: Optional[UnitsLength] = UnitsLength("µm")
    plane: List[Plane] = field(default_factory=list)
    significant_bits: Optional[PositiveInt] = None
    tiff_data: List[TiffData] = field(default_factory=list)
    time_increment: Optional[float] = None
    time_increment_unit: Optional[UnitsTime] = UnitsTime("s")
