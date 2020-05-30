from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Rights:
    rights_held: Optional[str] = None
    rights_holder: Optional[str] = None
