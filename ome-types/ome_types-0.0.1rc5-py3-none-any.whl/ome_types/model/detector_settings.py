from typing import Optional

from pydantic.dataclasses import dataclass

from .settings import Settings
from .simple_types import (
    Binning,
    DetectorID,
    PositiveInt,
    UnitsElectricPotential,
    UnitsFrequency,
)

_no_default = object()


@dataclass
class DetectorSettings(Settings):
    id: DetectorID = _no_default  # type: ignore
    binning: Optional[Binning] = None
    gain: Optional[float] = None
    integration: Optional[PositiveInt] = None
    offset: Optional[float] = None
    read_out_rate: Optional[float] = None
    read_out_rate_unit: Optional[UnitsFrequency] = UnitsFrequency("MHz")
    voltage: Optional[float] = None
    voltage_unit: Optional[UnitsElectricPotential] = UnitsElectricPotential(
        "V"
    )
    zoom: Optional[float] = None

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
