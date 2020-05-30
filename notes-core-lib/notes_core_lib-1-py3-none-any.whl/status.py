from enum import Enum

class Status(Enum):
    CREATED = 1
    STARTED = 2
    COMPLETED = 3
    SUSPENDED = 4
    CANCELED = 5
    DELETED = 6
