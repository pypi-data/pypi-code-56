from pydantic.dataclasses import dataclass

from .annotation import Annotation
from .map import Map

_no_default = object()


@dataclass
class MapAnnotation(Annotation):
    value: Map = _no_default  # type: ignore

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.value is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'value'")
