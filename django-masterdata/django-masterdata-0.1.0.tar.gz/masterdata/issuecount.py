from typing import NamedTuple
from .check import Check


class IssueCount(NamedTuple):
    check: Check
    count: int
