"""Cowsay raster dataset metdata items"""

import sys

import click
import rasterio
import json

from colormap import __version__ as colormap_version


@click.command(short_help="Cowsay some dataset metadata.")
@click.argument('inputfile', type=click.Path(resolve_path=True), required=True,
                metavar="INPUT")
@click.option('--band', default=1, help="Select a band.")
@click.version_option(version=colormap_version, message='%(version)s')
@click.pass_context
def colormap(ctx, inputfile, band):
    """Moo some dataset metadata to stdout.

    Python module: rio-metasay
    (https://github.com/sgillies/rio-plugin-example).
    """
    with rasterio.open(inputfile) as src:
        meta = src.profile
        try:
            d = src.colormap(band)
            ret = json.dumps(d, indent=2)
            click.echo(ret)
        except Exception as e:
            click.echo(e)
    
