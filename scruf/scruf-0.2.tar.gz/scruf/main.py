"""Main entry point for CLI application"""
import argparse
import re
import sys

from scruf.runners import cli


def run(argv):
    """Run scruf with options over some files

    Exits via `sys.exit` with 1 if tests fail, otherwise 0
    """
    options = _get_options(argv[1:])
    filenames = options.pop("files")

    exit_code = 0 if cli.run_files(filenames, options) else 1
    sys.exit(exit_code)


def _get_options(args):
    parser = argparse.ArgumentParser(description="Placeholder")
    parser.add_argument("files", metavar="FILE", nargs="+", help="Files to be tested")
    parser.add_argument(
        "--no-cleanup",
        action="store_false",
        dest="cleanup",
        help="Avoid cleaning up temporary test directory",
    )
    parser.add_argument(
        "-s",
        "--shell",
        type=str,
        help="Path to shell to be used to run tests with",
        default="/bin/sh",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=_indent_arg_type,
        default="    ",
        help="String to be used for detecting indentation when parsing tests",
    )

    return vars(parser.parse_args(args))


def _indent_arg_type(string):
    # Convert literal "\t" to tab characters, e.g. for "--indent '\t'"
    string = re.sub(r"\\t", "\t", string)

    if not string.isspace():
        msg = "{} is not entirely whitespace".format(string)
        raise argparse.ArgumentTypeError(msg)
    return string
