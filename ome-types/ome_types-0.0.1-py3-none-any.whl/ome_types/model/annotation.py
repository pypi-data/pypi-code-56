from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .simple_types import AnnotationID, ExperimenterID


@dataclass
class Annotation:
    id: AnnotationID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    annotator: Optional[ExperimenterID] = None
    description: Optional[str] = None
    namespace: Optional[str] = None
