import glob
import logging
import os
import subprocess
from enum import Enum
from typing import Optional

import tqdm

DD_COMMAND = "/bin/dd if={src} of={dst} bs=1024k >& /dev/null"
RM_COMMAND = "/bin/rm {src}"
ECHO_COMMAND = "echo -ne '{progress}\\r'"

INFO = "dd+rm files:"


class Method(Enum):
    BASH = 1
    SUBPROCESS = 2


def pydd(
    src_dir: str,
    regex: str,
    dst_dir: str,
    disable_progressbar: Optional[bool] = False,
    method: Optional[Method] = Method.BASH,
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
    :param method: Method
        Either Method.BASH or Method.SUBPROCESS
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

    if method is Method.SUBPROCESS:
        call_dd_with_subprocess(files, disable_progressbar, src_dir, dst_dir)
    elif method is Method.BASH:
        call_dd_in_bashfile(files, disable_progressbar, src_dir, dst_dir)
    else:
        raise ValueError(f"Invalid method {method} chosen")

    logging.info("\N{grinning face} File moving complete \N{grinning face}")


def get_src_and_dst_fnames(fpath, src_dir, dst_dir):
    fname = os.path.basename(fpath)
    src = os.path.join(src_dir, fname)
    dst = os.path.join(dst_dir, fname)
    return src, dst


def percent_progress(cur_num, total_num):
    return round(100 * cur_num / total_num)


def progress(cur_num, total_num):
    p = percent_progress(cur_num, total_num)
    bar = "#" * int(p / 5) + " " * (20 - int(p / 5))
    return f"{INFO}: {p}%: [{bar}] ({cur_num}/{total_num} files)"


def call_dd_with_subprocess(files, disable_progressbar, src_dir, dst_dir):
    commands = get_commands(files, src_dir, dst_dir)
    progress_bar = tqdm.tqdm(commands, disable=disable_progressbar)
    progress_bar.set_description(INFO)
    for cmd in progress_bar:
        subprocess.call(cmd, shell=True)


def get_commands(files, src_dir, dst_dir, echo_progress=False):
    commands = []
    num_files = len(files)
    for idx, f in enumerate(files):
        src, dst = get_src_and_dst_fnames(f, src_dir, dst_dir)
        if echo_progress and percent_progress(idx, num_files) % 10 == 0:
            commands.append(ECHO_COMMAND.format(progress=progress(idx, num_files)))
        commands.append(DD_COMMAND.format(src=src, dst=dst))
        commands.append(RM_COMMAND.format(src=src))
    return commands


def call_dd_in_bashfile(files, disable_progressbar, src_dir, dst_dir):
    bash_file_name = "fast_dd_mover.sh"
    commands = get_commands(
        files, src_dir, dst_dir, echo_progress=not disable_progressbar
    )
    with open(bash_file_name, "w") as bash_file:
        commands = ["#!/bin/bash"] + commands
        contents = map(lambda x: x + "\n", commands)
        bash_file.writelines(contents)
    subprocess.call(f"bash {bash_file_name}", shell=True)
    subprocess.call(f"/bin/rm {bash_file_name}", shell=True)
