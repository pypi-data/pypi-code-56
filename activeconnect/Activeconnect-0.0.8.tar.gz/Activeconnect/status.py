from enum import Enum


class Status(Enum):
    pending = 1
    timeout = 2
    closed = 3
    failed = 4
    walkaway = 5
    active = 6
    identifying = 7
    cancelled = 8