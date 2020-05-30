from pydantic.dataclasses import dataclass

from .light_source import LightSource


@dataclass
class LightEmittingDiode(LightSource):
    pass
