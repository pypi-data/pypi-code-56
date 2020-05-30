from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class ManufacturerSpec:
    lot_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
