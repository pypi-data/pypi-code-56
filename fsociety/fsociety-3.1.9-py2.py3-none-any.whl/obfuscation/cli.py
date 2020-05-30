# Core
from fsociety.core.menu import tools_cli

from .cuteit import cuteit

__tools__ = [str(tool) for tool in [cuteit]]


def cli():
    tools_cli(__name__, __tools__)
