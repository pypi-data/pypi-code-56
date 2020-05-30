from pydantic.dataclasses import dataclass

from .annotation import Annotation


@dataclass
class BasicAnnotation(Annotation):
    pass
