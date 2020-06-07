import logging

import click

logger = logging.getLogger(__name__)


@click.command()
@click.argument("conda_packages", metavar="CONDA_PACKAGE",
                type=click.Path(exists=True, dir_okay=False), nargs=-1)
@click.option("--label", metavar="LABEL", default="main", show_default=True, help="Add the package to a specific label.")
@click.option("--conflict", type=click.Choice(["fail", "ask", "overwrite", "skip"]), default="fail", show_default=True,
              help="Strategy to use when package already exists on server.",
              )
def upload(conda_packages, label, conflict):
    """Uploads a Conda package to a Carlae Server"""
    from . import upload
    config = upload.CarlaeSettings(
        hostname="127.0.0.1",
        port=2121,
        # TODO: Take these from netrc
        username="lisa",
        password="123",
    )
    try:
        upload.upload(config, conda_packages, label=label, conflict=conflict)
    except Exception as e:
        logger.error(e)
        return -1
