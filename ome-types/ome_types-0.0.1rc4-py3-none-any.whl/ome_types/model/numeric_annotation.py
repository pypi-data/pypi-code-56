from pydantic.dataclasses import dataclass

from .basic_annotation import BasicAnnotation


@dataclass
class NumericAnnotation(BasicAnnotation):
    pass
