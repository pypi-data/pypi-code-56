from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass
from pydantic.types import conlist

from .annotation_ref import AnnotationRef
from .shape import Shape
from .simple_types import ROIID


@dataclass
class ROI:
    id: ROIID
    union: conlist(Shape, min_items=1)
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    name: Optional[str] = None
