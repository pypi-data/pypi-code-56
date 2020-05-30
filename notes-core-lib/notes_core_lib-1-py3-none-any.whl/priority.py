from enum import Enum

class Priority(Enum):
    MINOR = (1, 'MINOR', 'Minor')
    NORMAL = (2, 'NORMAL', 'Normal')
    IMPORTANT = (3, 'IMPORTANT', 'Important')
