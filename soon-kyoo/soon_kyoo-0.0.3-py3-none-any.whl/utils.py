"""Utility functionalities.

Defines:
echo
"""

import functools

import click


def echo(*args, **kwargs):
    return click.echo(*args, **kwargs)


functools.update_wrapper(echo, click.echo)
