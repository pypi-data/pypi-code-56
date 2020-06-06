import argparse
from typing import List


def parse_args(args: List[str]) -> argparse.Namespace:
    """ Parses user cli input.

    :param args: Namespace
        The parsed user input placed into a Namespace
    :return: Namespace
        The parsed user args
    """
    parser = argparse.ArgumentParser(description="Fast move of files")
    parser.add_argument(
        "--src", type=str, help="src dir to move files from", required=True
    )
    parser.add_argument(
        "--dst", type=str, help="dst dir to move files to", required=True
    )
    parser.add_argument(
        "--regex", type=str, help="glob regex for file (eg *.txt)", required=True
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="decrease output verbosity",
    )
    return parser.parse_args(args)
