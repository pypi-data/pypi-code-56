from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import FilterID
from .transmittance_range import TransmittanceRange


class Type(Enum):
    BAND_PASS = "BandPass"
    DICHROIC = "Dichroic"
    LONG_PASS = "LongPass"
    MULTI_PASS = "MultiPass"
    NEUTRAL_DENSITY = "NeutralDensity"
    OTHER = "Other"
    SHORT_PASS = "ShortPass"
    TUNEABLE = "Tuneable"


_no_default = object()


@dataclass
class Filter(ManufacturerSpec):
    id: FilterID = _no_default  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    filter_wheel: Optional[str] = None
    transmittance_range: Optional[TransmittanceRange] = None
    type: Optional[Type] = None

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
