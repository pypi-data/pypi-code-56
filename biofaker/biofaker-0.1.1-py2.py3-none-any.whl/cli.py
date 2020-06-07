#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import sys
import click

from biofaker.biofaker import BioFaker


@click.group()
@click.version_option()
@click.pass_context
def main(ctx):
    """ BioFaker: create fake biological data. """
    ctx.obj = BioFaker()


@main.command()
@click.option("--length", "-l", default=10, show_default=True, type=int,
              help="Length of the sequence")
@click.option("--alphabet", "-a", default="unambiguous", show_default=True,
              type=click.Choice(["ambiguous", "extended", "unambiguous"]),
              help="Alphabet to use")
@click.pass_obj
def dna(ctx, length, alphabet):
    """ Create a random DNA sequence. """
    sequence = ctx.dna(length=length, alphabet=alphabet)
    click.echo(sequence)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
