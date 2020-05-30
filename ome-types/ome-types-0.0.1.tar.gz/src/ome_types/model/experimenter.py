from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .simple_types import ExperimenterID


@dataclass
class Experimenter:
    id: ExperimenterID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    email: Optional[str] = None
    first_name: Optional[str] = None
    institution: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    user_name: Optional[str] = None
