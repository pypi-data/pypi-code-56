from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .dataset import Dataset
from .experiment import Experiment
from .experimenter import Experimenter
from .experimenter_group import ExperimenterGroup
from .folder import Folder
from .image import Image
from .instrument import Instrument
from .plate import Plate
from .project import Project
from .rights import Rights
from .roi import ROI
from .screen import Screen
from .simple_types import UniversallyUniqueIdentifier
from .structured_annotations import StructuredAnnotations


@dataclass
class BinaryOnly:
    metadata_file: str
    uuid: UniversallyUniqueIdentifier


@dataclass
class OME:
    binary_only: Optional[BinaryOnly] = None
    creator: Optional[str] = None
    dataset: List[Dataset] = field(default_factory=list)
    experiment: List[Experiment] = field(default_factory=list)
    experimenter: List[Experimenter] = field(default_factory=list)
    experimenter_group: List[ExperimenterGroup] = field(default_factory=list)
    folder: List[Folder] = field(default_factory=list)
    image: List[Image] = field(default_factory=list)
    instrument: List[Instrument] = field(default_factory=list)
    plate: List[Plate] = field(default_factory=list)
    project: List[Project] = field(default_factory=list)
    rights: Optional[Rights] = None
    roi: List[ROI] = field(default_factory=list)
    screen: List[Screen] = field(default_factory=list)
    structured_annotations: Optional[StructuredAnnotations] = None
    uuid: Optional[UniversallyUniqueIdentifier] = None
