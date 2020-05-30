from dataclasses import field
from typing import List

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import DichroicID

_no_default = object()


@dataclass
class Dichroic(ManufacturerSpec):
    id: DichroicID = _no_default  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
