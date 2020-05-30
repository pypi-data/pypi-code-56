from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from .manufacturer_spec import ManufacturerSpec


class Type(Enum):
    DISSECTION = "Dissection"
    ELECTROPHYSIOLOGY = "Electrophysiology"
    INVERTED = "Inverted"
    OTHER = "Other"
    UPRIGHT = "Upright"


@dataclass
class Microscope(ManufacturerSpec):
    type: Optional[Type] = None
