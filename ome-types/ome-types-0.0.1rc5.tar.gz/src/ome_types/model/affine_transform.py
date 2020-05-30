from pydantic.dataclasses import dataclass


@dataclass
class AffineTransform:
    a00: float
    a01: float
    a02: float
    a10: float
    a11: float
    a12: float
