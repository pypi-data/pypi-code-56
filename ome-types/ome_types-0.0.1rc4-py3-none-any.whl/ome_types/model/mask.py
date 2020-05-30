from pydantic.dataclasses import dataclass

from .bin_data import BinData
from .shape import Shape

_no_default = object()


@dataclass
class Mask(Shape):
    bin_data: BinData = _no_default  # type: ignore
    height: float = _no_default  # type: ignore
    width: float = _no_default  # type: ignore
    x: float = _no_default  # type: ignore
    y: float = _no_default  # type: ignore

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.height is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'height'")
        if self.y is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'y'")
        if self.bin_data is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'bin_data'")
        if self.x is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'x'")
        if self.width is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'width'")
