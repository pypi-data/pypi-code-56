from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .experimenter_ref import ExperimenterRef
from .microbeam_manipulation import MicrobeamManipulation
from .simple_types import ExperimentID


@dataclass
class Experiment:
    id: ExperimentID
    description: Optional[str] = None
    experimenter_ref: Optional[ExperimenterRef] = None
    microbeam_manipulation: List[MicrobeamManipulation] = field(
        default_factory=list
    )
    type = None
