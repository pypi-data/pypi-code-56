from pydantic.dataclasses import dataclass

from .shape import Shape

_no_default = object()


@dataclass
class Polygon(Shape):
    points: str = _no_default  # type: ignore

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.points is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'points'")
