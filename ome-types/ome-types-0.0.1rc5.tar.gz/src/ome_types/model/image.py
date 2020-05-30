from dataclasses import field
from datetime import datetime
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .experiment_ref import ExperimentRef
from .experimenter_group_ref import ExperimenterGroupRef
from .experimenter_ref import ExperimenterRef
from .imaging_environment import ImagingEnvironment
from .instrument_ref import InstrumentRef
from .microbeam_manipulation_ref import MicrobeamManipulationRef
from .objective_settings import ObjectiveSettings
from .pixels import Pixels
from .roi_ref import ROIRef
from .simple_types import ImageID
from .stage_label import StageLabel


@dataclass
class Image:
    id: ImageID
    pixels: Pixels
    acquisition_date: Optional[datetime] = None
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    experiment_ref: Optional[ExperimentRef] = None
    experimenter_group_ref: Optional[ExperimenterGroupRef] = None
    experimenter_ref: Optional[ExperimenterRef] = None
    imaging_environment: Optional[ImagingEnvironment] = None
    instrument_ref: Optional[InstrumentRef] = None
    microbeam_manipulation_ref: List[MicrobeamManipulationRef] = field(
        default_factory=list
    )
    name: Optional[str] = None
    objective_settings: Optional[ObjectiveSettings] = None
    roi_ref: List[ROIRef] = field(default_factory=list)
    stage_label: Optional[StageLabel] = None
