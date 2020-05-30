from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .reagent import Reagent
from .reference import Reference
from .simple_types import PlateID, ScreenID

_no_default = object()


@dataclass
class PlateRef(Reference):
    id: PlateID = _no_default  # type: ignore

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")


@dataclass
class Screen:
    id: ScreenID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    name: Optional[str] = None
    plate_ref: List[PlateRef] = field(default_factory=list)
    protocol_description: Optional[str] = None
    protocol_identifier: Optional[str] = None
    reagent: List[Reagent] = field(default_factory=list)
    reagent_set_description: Optional[str] = None
    reagent_set_identifier: Optional[str] = None
    type: Optional[str] = None
