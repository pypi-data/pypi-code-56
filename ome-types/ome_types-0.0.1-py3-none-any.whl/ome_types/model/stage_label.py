from typing import Optional

from pydantic.dataclasses import dataclass

from .simple_types import UnitsLength


@dataclass
class StageLabel:
    name: str
    x: Optional[float] = None
    x_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    y: Optional[float] = None
    y_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    z: Optional[float] = None
    z_unit: Optional[UnitsLength] = UnitsLength("reference frame")
