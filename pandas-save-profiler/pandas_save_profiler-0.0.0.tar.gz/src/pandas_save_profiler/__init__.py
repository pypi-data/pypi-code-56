"""
Evaluate pandas saving function in terms of:

- time
- memory usage
- file size

"""

from .save_profiler import save_profiler
from ._humanize import _humanize

__version__ = '0.0.0'

__all__ = [
    'save_profiler',
    '_humanize',
]
