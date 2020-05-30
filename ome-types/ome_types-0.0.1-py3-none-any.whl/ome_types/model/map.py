from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class M:
    k: Optional[str] = None


@dataclass
class Map:
    k: Optional[str] = None
    m: List[M] = field(default_factory=list)
