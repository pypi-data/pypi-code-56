from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .simple_types import Hex40, NonNegativeInt, UnitsLength, UnitsTime


@dataclass
class Plane:
    the_c: NonNegativeInt
    the_t: NonNegativeInt
    the_z: NonNegativeInt
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    delta_t: Optional[float] = None
    delta_t_unit: Optional[UnitsTime] = UnitsTime("s")
    exposure_time: Optional[float] = None
    exposure_time_unit: Optional[UnitsTime] = UnitsTime("s")
    hash_sha1: Optional[Hex40] = None
    position_x: Optional[float] = None
    position_x_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    position_y: Optional[float] = None
    position_y_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    position_z: Optional[float] = None
    position_z_unit: Optional[UnitsLength] = UnitsLength("reference frame")
