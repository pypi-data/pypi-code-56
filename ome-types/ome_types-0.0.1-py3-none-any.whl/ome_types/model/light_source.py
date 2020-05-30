from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import LightSourceID, UnitsPower

_no_default = object()


@dataclass
class LightSource(ManufacturerSpec):
    id: LightSourceID = _no_default  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    power: Optional[float] = None
    power_unit: Optional[UnitsPower] = UnitsPower("mW")

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
