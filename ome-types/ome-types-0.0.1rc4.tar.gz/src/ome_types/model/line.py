from typing import Optional

from pydantic.dataclasses import dataclass

from .shape import Shape
from .simple_types import Marker

_no_default = object()


@dataclass
class Line(Shape):
    x1: float = _no_default  # type: ignore
    x2: float = _no_default  # type: ignore
    y1: float = _no_default  # type: ignore
    y2: float = _no_default  # type: ignore
    marker_end: Optional[Marker] = None
    marker_start: Optional[Marker] = None

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.y2 is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'y2'")
        if self.x1 is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'x1'")
        if self.x2 is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'x2'")
        if self.y1 is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'y1'")
