from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .reagent_ref import ReagentRef
from .simple_types import Color, NonNegativeInt, WellID
from .well_sample import WellSample


@dataclass
class Well:
    column: NonNegativeInt
    id: WellID
    row: NonNegativeInt
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    color: Optional[Color] = -1
    external_description: Optional[str] = None
    external_identifier: Optional[str] = None
    reagent_ref: Optional[ReagentRef] = None
    type: Optional[str] = None
    well_sample: List[WellSample] = field(default_factory=list)
