from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .basic_annotation import BasicAnnotation

_no_default = object()


@dataclass
class BooleanAnnotation(BasicAnnotation):
    value: bool = _no_default  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.value is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'value'")
