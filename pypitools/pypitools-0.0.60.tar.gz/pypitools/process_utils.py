import logging
import subprocess
import sys
from typing import List, Tuple


def check_call_no_output(args: List[str]) -> None:
    """
    Run a process and check that it returns an OK return code
    The process may have output but that will not fail this function
    nor be shown on the screen (unless the subprocess returns an error
    code).
    :param args:
    """
    logger = logging.getLogger(__name__)
    logger.debug("running %s", args)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
    (res_stdout, res_stderr) = process.communicate()
    if process.returncode:
        print(res_stdout.decode(), end="", file=sys.stdout)
        print(res_stderr.decode(), end="", file=sys.stderr)
        raise ValueError(
            "exit code from [{}] was [{}]".format(" ".join(args), process.returncode)
        )


def check_call_collect(args: List[str]) -> Tuple[str, str]:
    """
    Run a process and check that it returns an OK return code
    Gather any output and return it to the caller.
    If the process returns an error then print the output and
    the errors.
    :param args:
    """
    logger = logging.getLogger(__name__)
    logger.debug("running %s", args)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
    (res_stdout, res_stderr) = process.communicate()
    if process.returncode:
        print(res_stdout.decode(), end="", file=sys.stdout)
        print(res_stderr.decode(), end="", file=sys.stderr)
        raise ValueError(
            "exit code from [{}] was [{}]".format(" ".join(args), process.returncode)
        )
    return res_stdout.decode(), res_stderr.decode()
