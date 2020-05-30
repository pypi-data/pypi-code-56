from pydantic.dataclasses import dataclass

from .shape import Shape

_no_default = object()


@dataclass
class Point(Shape):
    x: float = _no_default  # type: ignore
    y: float = _no_default  # type: ignore

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.x is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'x'")
        if self.y is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'y'")
