from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .simple_types import ReagentID


@dataclass
class Reagent:
    id: ReagentID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    name: Optional[str] = None
    reagent_identifier: Optional[str] = None
