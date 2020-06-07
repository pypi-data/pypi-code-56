#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create and manage command-line arguments parser, using std argparse.
"""

import argparse
import os

from prettyetc.etccore import __version__ as etccore_version

__all__ = ("create_parser", "parse_args")


def create_parser() -> argparse.ArgumentParser:
    """A factory function for creating standard argparsers."""
    parser = argparse.ArgumentParser(
        prefix_chars='-',
        prog="prettyetc",
        description="Show your configs files using the %(prog)s project.",
        epilog="The project is released under the GNU GPL 3.0")
    parser.add_argument(
        "paths",
        help="Input files, these are opened directly to ui if are valid,"
        "otherwise if doesn't exist or is not valid files, show an error",
        nargs="*",
        default=[],
        type=lambda path: path if os.path.isfile(path) else None)
    parser.add_argument(
        '--version',
        action='version',
        version="The %(prog)s project\n"
        "Core version {}".format(etccore_version))

    plugingroup = parser.add_argument_group("Plugin options")
    plugingroup.add_argument(
        "--plugin-path",
        "-p",
        action="append",
        dest="plugin_paths",
        default=[],
        help="Add an extra plugin path to the plugin manager")
    plugingroup.add_argument(
        "--plugin-file",
        "--pf",
        action="append",
        dest="plugin_files",
        default=[],
        help="Add an extra plugin module to the plugin manager")

    logging_group = parser.add_argument_group("Login options")
    logging_group.add_argument(
        "--log-file", dest="logfile", help="Set log file.")
    logging_group.add_argument(
        "--logger-name",
        dest="loggername",
        default="prettyetc",
        help="Set root logger name.\n"
        "This options is intended to be used for the developers as debug feature."
    )

    verbosity_exc_group = logging_group.add_mutually_exclusive_group()
    verbosity_exc_group.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbose",
        default=0,
        help="Increase verbosity.\n"
        "If 3 -v (or -vvv) is given, some unexpected dev features can be activated."
    )
    verbosity_exc_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        dest="quiet",
        help="Show only errors.")

    # Coming soon
    # output_group = parser.add_argument_group("Output options")
    # output_group.add_argument(
    #     "--tree",
    #     dest="tree",
    #     action="store_true",
    #     help="Show given file as a tree (ASCII tree)")
    return parser


def parse_args(args: list = None,
               parser: argparse.ArgumentParser = create_parser()
              ) -> argparse.Namespace:
    """Parse command-line arguments."""
    parsed = parser.parse_known_args(args)
    return parsed[0]
