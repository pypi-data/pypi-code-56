# -*- coding: utf-8 -*-
"""Module to move files using 'dd'

This module uses dd and then rm to
1. Copy files from a src dir to a dst dir
2. Remove the files from the src dir.

Example:
    $ pydd --src /Documents/data/ --dst Documents/archive/ --regex *.dat

    This moves files that match the regex /Documents/data/*.dat to Documents/archive/
"""

import argparse
import glob
import logging
import os
import subprocess
import sys
from typing import List, Optional

import tqdm

DD_COMMAND = "/bin/dd if={src} of={dst} bs=1024k >& /dev/null"
RM_COMMAND = "/bin/rm {src}"


def set_logger_mode(quiet_mode: bool) -> None:
    """ Configure the logger to be in debug/info mode.

    :param quiet_mode: bool
        if true, configures the logger to allow only "ERROR" level logs
    :return: None
    """
    if quiet_mode:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def pydd(
    src_dir: str, regex: str, dst_dir: str, disable_progressbar: Optional[bool] = False
) -> None:
    """Find the files and executes the dd and rm on them.

    :param src_dir: str
        The dir where the files are searched
    :param regex: str
        The search regex
    :param dst_dir: str
        The dir where the files are to be moved
    :param disable_progressbar: bool
        If True, disables the tqdm progress bar
    :return: None
    """
    logging.info("Searching for files to move...")
    search_str = os.path.join(src_dir, regex)
    files = glob.glob(search_str)
    if len(files) == 0:
        logging.error(
            f"No files found \N{worried face}." f" Search param: {search_str}"
        )
        return

    logging.info(f"Moving {len(files)} files from {src_dir}-->{dst_dir}")
    os.makedirs(dst_dir, exist_ok=True)
    progress_bar = tqdm.tqdm(files, disable=disable_progressbar)
    progress_bar.set_description("Moving files")
    for f in progress_bar:
        fname = os.path.basename(f)
        src = os.path.join(src_dir, fname)
        dst = os.path.join(dst_dir, fname)
        subprocess.call(DD_COMMAND.format(src=src, dst=dst), shell=True)
        subprocess.call(RM_COMMAND.format(src=src), shell=True)
    logging.info("\N{grinning face} File moving complete \N{grinning face}")


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


def main():
    args = parse_args(sys.argv[1:])
    set_logger_mode(quiet_mode=args.quiet)
    pydd(
        src_dir=args.src,
        dst_dir=args.dst,
        regex=args.regex,
        disable_progressbar=args.quiet,
    )
