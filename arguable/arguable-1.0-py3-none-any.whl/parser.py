from argparse import ArgumentParser

from .base import Arguable


class FullHelpParser(ArgumentParser):
    """Parser which uses `Arguable.super_parser` to display the help text."""

    def print_help(self, file=None):
        """Print help text from `Arguable.super_parser`."""
        Arguable.super_parser.print_help(file=file)
