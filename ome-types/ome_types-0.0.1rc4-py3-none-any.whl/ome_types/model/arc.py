from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from .light_source import LightSource


class Type(Enum):
    HG = "Hg"
    HG_XE = "HgXe"
    OTHER = "Other"
    XE = "Xe"


@dataclass
class Arc(LightSource):
    type: Optional[Type] = None
