from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .dichroic_ref import DichroicRef
from .filter_ref import FilterRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import FilterSetID

_no_default = object()


@dataclass
class FilterSet(ManufacturerSpec):
    id: FilterSetID = _no_default  # type: ignore
    dichroic_ref: Optional[DichroicRef] = None
    emission_filter_ref: List[FilterRef] = field(default_factory=list)
    excitation_filter_ref: List[FilterRef] = field(default_factory=list)

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
