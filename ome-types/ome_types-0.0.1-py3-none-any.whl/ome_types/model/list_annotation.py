from pydantic.dataclasses import dataclass

from .annotation import Annotation


@dataclass
class ListAnnotation(Annotation):
    pass
