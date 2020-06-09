
import subprocess
import shlex
from dataclasses import dataclass


def run_command(command, stdout=None, in_dir=None):

    command_split = shlex.split(command)
    result = subprocess.call(command_split, stdout=stdout, cwd=in_dir)

    return True


def run_and_get_shell_result(command):

    status, output = subprocess.getstatusoutput()
    return True


@dataclass()
class ShellResult:

    one: str




