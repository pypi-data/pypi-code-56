from datetime import datetime
from typing import Optional

from pydantic.dataclasses import dataclass

from .image_ref import ImageRef
from .simple_types import NonNegativeInt, UnitsLength, WellSampleID


@dataclass
class WellSample:
    id: WellSampleID
    index: NonNegativeInt
    image_ref: Optional[ImageRef] = None
    position_x: Optional[float] = None
    position_x_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    position_y: Optional[float] = None
    position_y_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    timepoint: Optional[datetime] = None
