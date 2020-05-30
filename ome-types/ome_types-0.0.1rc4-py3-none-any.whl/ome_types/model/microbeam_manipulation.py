from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .experimenter_ref import ExperimenterRef
from .light_source_settings import LightSourceSettings
from .roi_ref import ROIRef
from .simple_types import MicrobeamManipulationID


@dataclass
class MicrobeamManipulation:
    experimenter_ref: ExperimenterRef
    id: MicrobeamManipulationID
    roi_ref: List[ROIRef]
    description: Optional[str] = None
    light_source_settings: List[LightSourceSettings] = field(
        default_factory=list
    )
    type = None
