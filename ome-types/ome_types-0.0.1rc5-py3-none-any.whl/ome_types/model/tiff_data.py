from typing import Optional

from pydantic.dataclasses import dataclass

from .simple_types import NonNegativeInt, UniversallyUniqueIdentifier


@dataclass
class TiffData:
    uuid: Optional[
        dataclass(
            type(
                "UUID",
                (),
                {
                    "__annotations__": {
                        "file_name": str,
                        "value": UniversallyUniqueIdentifier,
                    }
                },
            )
        )
    ]
    first_c: Optional[NonNegativeInt] = 0
    first_t: Optional[NonNegativeInt] = 0
    first_z: Optional[NonNegativeInt] = 0
    ifd: Optional[NonNegativeInt] = 0
    plane_count: Optional[NonNegativeInt] = None
