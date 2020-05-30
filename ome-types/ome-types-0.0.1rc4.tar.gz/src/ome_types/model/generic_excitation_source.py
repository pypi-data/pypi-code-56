from typing import Optional

from pydantic.dataclasses import dataclass

from .light_source import LightSource
from .map import Map


@dataclass
class GenericExcitationSource(LightSource):
    map: Optional[Map] = None
