import netrc

import click
import click_params

from carlae.cli import logger


@click.command()
@click.option(
    "-h", "--hostname", prompt=True, help="The Carlae Server domain", type=click_params.DOMAIN
)
@click.option(
    "-p", "--port",
    help="The Carlae Server port",
    type=click.IntRange(1, 65535),
    default=21,
    show_default=True,
)
@click.option(
    "-l", "--label",
    metavar="LABEL",
    default="main",
    show_default=True,
    help="Upload packages to a specific label.",
)
@click.option(
    "--conflict",
    type=click.Choice(["fail", "ask", "overwrite", "skip"]),
    default="fail",
    show_default=True,
    help="Strategy to use when package already exists.",
)
@click.argument(
    "conda_packages",
    metavar="CONDA_PACKAGE",
    type=click.Path(exists=True, dir_okay=False),
    nargs=-1,
)
def upload(hostname, port, label, conflict, conda_packages):
    """Uploads a Conda package to a Carlae Server"""
    from . import upload

    rc = netrc.netrc()
    username, _, password = rc.authenticators(hostname)

    config = upload.CarlaeSettings(
        hostname=hostname, port=port, username=username, password=password,
    )
    try:
        upload.upload(config, conda_packages, label=label, conflict=conflict)
    except Exception as e:
        logger.error(e)
        return -1
