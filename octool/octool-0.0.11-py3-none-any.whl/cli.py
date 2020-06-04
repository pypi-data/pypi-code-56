# Copyright (C) 2020 jumanjiman (Paul Morgan) <jumanjiman@gmail.com>
#
# This file is part of octool.
#
# octool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# octool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with octool.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""CLI utility for OCTool."""
import argparse
import logging
import os
import sys
from textwrap import dedent

from .version import URL
from .version import VERSION

DESCRIPTION = dedent(
    """\
    Open Compliance Tool
    """,
)

EPILOG = dedent(
    """\
    This (Python) version is a placeholder for a port from the Ruby version.
    See https://github.com/jumanjihouse/octool
    """,
)


class Cli:
    """Provide a command-line-interface for octool."""

    def __init__(self):
        """Return a new instance of the CLI."""
        self.build_parser()
        logging.basicConfig(
            format="[%(levelname)s] %(message)s",
            level=logging.DEBUG if "DEBUG" in os.environ else logging.WARNING,
        )

    def main(self):
        """Run the CLI."""
        args = self.parser.parse_args()

    def build_parser(self):
        """Private method to return the CLI argument parser."""
        parser = argparse.ArgumentParser(
            description=DESCRIPTION,
            epilog=EPILOG,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"octool {VERSION} {URL}",
        )
        self.parser = parser
