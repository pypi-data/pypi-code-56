from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .detector import Detector
from .dichroic import Dichroic
from .filter import Filter
from .filter_set import FilterSet
from .light_source import LightSource
from .light_source_group import LightSourceGroup
from .microscope import Microscope
from .objective import Objective
from .simple_types import InstrumentID


@dataclass
class Instrument:
    id: InstrumentID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    detector: List[Detector] = field(default_factory=list)
    dichroic: List[Dichroic] = field(default_factory=list)
    filter: List[Filter] = field(default_factory=list)
    filter_set: List[FilterSet] = field(default_factory=list)
    light_source_group: List[LightSourceGroup] = field(default_factory=list)
    microscope: Optional[Microscope] = None
    objective: List[Objective] = field(default_factory=list)
