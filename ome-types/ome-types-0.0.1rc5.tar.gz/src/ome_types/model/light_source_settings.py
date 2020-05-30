from typing import Optional

from pydantic.dataclasses import dataclass

from .settings import Settings
from .simple_types import (
    LightSourceID,
    PercentFraction,
    PositiveFloat,
    UnitsLength,
)

_no_default = object()


@dataclass
class LightSourceSettings(Settings):
    id: LightSourceID = _no_default  # type: ignore
    attenuation: Optional[PercentFraction] = None
    wavelength: Optional[PositiveFloat] = None
    wavelength_unit: Optional[UnitsLength] = UnitsLength("nm")

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
