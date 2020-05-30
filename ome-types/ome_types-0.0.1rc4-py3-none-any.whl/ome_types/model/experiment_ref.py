from pydantic.dataclasses import dataclass

from .reference import Reference
from .simple_types import ExperimentID

_no_default = object()


@dataclass
class ExperimentRef(Reference):
    id: ExperimentID = _no_default  # type: ignore

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
