from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from .light_source import LightSource


class Type(Enum):
    HALOGEN = "Halogen"
    INCANDESCENT = "Incandescent"
    OTHER = "Other"


@dataclass
class Filament(LightSource):
    type: Optional[Type] = None
