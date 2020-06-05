""" Deep Learning Package for Python

boris is a Python module for self-supervised active learning.

"""

__version__ = '0.0.dev0'

from .train_cli import train_cli
from .embed_cli import embed_cli
from .upload_cli import upload_cli

__all__ = [
    'data',
    'embedding',
    'loss',
    'models',
    'transforms'
]