from typing import Optional

from pydantic.dataclasses import dataclass

from .map import Map
from .simple_types import PercentFraction, UnitsPressure, UnitsTemperature


@dataclass
class ImagingEnvironment:
    air_pressure: Optional[float] = None
    air_pressure_unit: Optional[UnitsPressure] = UnitsPressure("mbar")
    co2_percent: Optional[PercentFraction] = None
    humidity: Optional[PercentFraction] = None
    map: Optional[Map] = None
    temperature: Optional[float] = None
    temperature_unit: Optional[UnitsTemperature] = UnitsTemperature("°C")
