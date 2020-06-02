from typing import NamedTuple, Optional


class ModuleAccumulation(NamedTuple):
    module_name: str
    touched_lines: int
    total_lines: Optional[int]
    is_accumulated: Optional[bool]
