from typing import Optional

from pydantic.dataclasses import dataclass

from .shape import Shape
from .simple_types import Marker

_no_default = object()


@dataclass
class Polyline(Shape):
    points: str = _no_default  # type: ignore
    marker_end: Optional[Marker] = None
    marker_start: Optional[Marker] = None

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.points is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'points'")
