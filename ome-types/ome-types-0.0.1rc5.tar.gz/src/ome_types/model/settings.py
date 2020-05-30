from pydantic.dataclasses import dataclass

from .reference import Reference


@dataclass
class Settings(Reference):
    pass
