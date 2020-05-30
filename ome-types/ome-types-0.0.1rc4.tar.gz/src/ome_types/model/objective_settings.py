from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from .settings import Settings
from .simple_types import ObjectiveID


class Medium(Enum):
    AIR = "Air"
    GLYCEROL = "Glycerol"
    OIL = "Oil"
    OTHER = "Other"
    WATER = "Water"


_no_default = object()


@dataclass
class ObjectiveSettings(Settings):
    id: ObjectiveID = _no_default  # type: ignore
    correction_collar: Optional[float] = None
    medium: Optional[Medium] = None
    refractive_index: Optional[float] = None

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
