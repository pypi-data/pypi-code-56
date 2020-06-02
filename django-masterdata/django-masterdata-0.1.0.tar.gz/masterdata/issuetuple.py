from typing import NamedTuple
from .check import Check


class IssueTuple(NamedTuple):
    obj: object
    check: Check
