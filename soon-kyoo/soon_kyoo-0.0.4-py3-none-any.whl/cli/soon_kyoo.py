"""Core command group.

Click groups:
soon_kyoo
"""

import click

from soon_kyoo.__version__ import __version__
from .init_db import init_db


@click.group()
@click.version_option(version=__version__, prog_name='soon-kyoo')
def soon_kyoo():
    """soon-kyoo: Simple queueing."""
    pass


soon_kyoo.add_command(init_db)
