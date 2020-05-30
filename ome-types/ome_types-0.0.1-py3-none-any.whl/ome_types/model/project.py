from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .dataset_ref import DatasetRef
from .experimenter_group_ref import ExperimenterGroupRef
from .experimenter_ref import ExperimenterRef
from .simple_types import ProjectID


@dataclass
class Project:
    id: ProjectID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    dataset_ref: List[DatasetRef] = field(default_factory=list)
    description: Optional[str] = None
    experimenter_group_ref: Optional[ExperimenterGroupRef] = None
    experimenter_ref: Optional[ExperimenterRef] = None
    name: Optional[str] = None
