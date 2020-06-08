"""Error representation and reporting"""
from dataclasses import dataclass
from enum import Enum


class UserErrorType(Enum):
    """A type of error that must be addressed by the programmer"""

    SYNTAX_ERROR = auto()
    COMPILER_ERROR = auto()
    RUNTIME_ERROR = auto()

    FFI_ERROR = auto()


@dataclass
class UserError:
    """An error that must be addressed by the Teal programmer"""

    error_type: UserErrorType

    source_file: str
    source_line: int
    source_column: int = None

    traceback: Any = None  # either Teal or python...?

    resolution_hint: str = None


@dataclass
class TealError:
    """An error in the Teal runtime"""

    exception_object: Exception
    description: str
    # machine_state ??
