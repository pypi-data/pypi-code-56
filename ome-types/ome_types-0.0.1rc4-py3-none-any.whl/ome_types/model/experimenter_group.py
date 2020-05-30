from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .experimenter_ref import ExperimenterRef
from .leader import Leader
from .simple_types import ExperimenterGroupID


@dataclass
class ExperimenterGroup:
    id: ExperimenterGroupID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    experimenter_ref: List[ExperimenterRef] = field(default_factory=list)
    leader: List[Leader] = field(default_factory=list)
    name: Optional[str] = None
