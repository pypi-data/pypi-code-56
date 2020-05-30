from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .folder_ref import FolderRef
from .image_ref import ImageRef
from .roi_ref import ROIRef
from .simple_types import FolderID


@dataclass
class Folder:
    id: FolderID
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    folder_ref: List[FolderRef] = field(default_factory=list)
    image_ref: List[ImageRef] = field(default_factory=list)
    name: Optional[str] = None
    roi_ref: List[ROIRef] = field(default_factory=list)
