"""Top-level package for Carlae's CLI."""
import logging

import click
import click_log
from click_plugins import with_plugins
from entrypoints import get_group_named

from ._version import version as __version__  # noqa: F401


logger = logging.getLogger("carlae")
click_log.basic_config(logger)


@with_plugins(get_group_named("carlae.cli").values())
@click.group(
    context_settings={"auto_envvar_prefix": "CARLAE", "max_content_width": 100,}
)
@click_log.simple_verbosity_option(logger, "--log-level", show_default=True)
def cli():
    """carlae command-line-interface"""
    return 0
