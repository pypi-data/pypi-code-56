from pydantic.dataclasses import dataclass

from .reference import Reference
from .simple_types import ImageID

_no_default = object()


@dataclass
class ImageRef(Reference):
    id: ImageID = _no_default  # type: ignore

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
