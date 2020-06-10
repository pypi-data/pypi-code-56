"""
The following module contains functions which can be used to execute one, or more commands (e.g.
PowerShell scripts, or sequences of bash commands).
"""

from subprocess import PIPE, TimeoutExpired
from typing import Union, List
from dataclasses import dataclass, field

import distutils.spawn
import subprocess
import os
import logging
import time
import psutil
import hodgepodge.helpers
import hodgepodge.path

from hodgepodge.helpers import ensure_type

logger = logging.getLogger(__name__)

#: The set of available command types.
SH = "sh"
BASH = "bash"
COMMAND_PROMPT = "command_prompt"
POWERSHELL = "powershell"
SUPPORTED_COMMAND_TYPES = [SH, BASH, COMMAND_PROMPT, POWERSHELL]

#: The default command type ("cmd.exe" on Windows, and bash on POSIX).
DEFAULT_COMMAND_TYPE = COMMAND_PROMPT if hodgepodge.helpers.platform_is_windows() else BASH

#: Shims to use when executing commands (e.g. to execute "ls" on Linux, execute "bash -c 'ls'").
COMMAND_TYPES_TO_COMMAND_LAUNCHERS = {
    SH: ['sh', '-c'],
    BASH: ['bash', '-c'],
    COMMAND_PROMPT: ['cmd', '/c'],
    POWERSHELL: ['powershell.exe'],
}

#: Default timeout for commands.
DEFAULT_COMMAND_TIMEOUT = 15


@dataclass(eq=False, frozen=False)
class CommandBlock:
    """
    This class is used to execute blocks of one or more commands, or individual commands (e.g.
    PowerShell scripts, or shell commands).
    """
    command: str
    command_type: str = None
    timeout: Union[int, float] = DEFAULT_COMMAND_TIMEOUT

    @property
    def type(self):
        """
        An alias for the command type associated with this command block.
        """
        return self.command_type

    def __call__(self):
        return execute_command(
            command=self.command,
            command_type=self.command_type,
            timeout=self.timeout,
        )

    def __hash__(self):
        return hash((self.command, self.command_type))

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
               (self.command, self.command_type) == (other.command, other.command_type)


@dataclass(eq=False, frozen=False)
class Command(CommandBlock):
    """
    This class is used to execute individual commands, and could be used to execute shell commands
    such as "ls -lah", or "rm -rf / --no-preserve-root" for those who are feeling adventurous.
    """
    @property
    def executable_path(self):
        """
        Looks up the path to the executable that will be used to execute the provided command.
        """
        return get_executable_path(self.command)

    @property
    def executable_name(self):
        """
        Looks up the name of the executable that will be used to execute the provided command.
        """
        return get_executable_name(self.command)


@dataclass(eq=False, frozen=True)
class ObservedProcess:
    """
    The following class is used to store information about observed processes.

    Example data sources include:
    - Windows Event Log
    - Linux audit framework
    - OpenBSM (macOS).
    - osquery.
    """
    pid: int
    ppid: int
    start_timestamp: float
    cwd: str
    name: Union[str, None]
    executable_path: Union[str, None]
    command_line: Union[str, None]
    child_processes: List["ObservedProcess"] = field(repr=False)

    def __eq__(self, other):
        return isinstance(other, ObservedProcess) and \
               (self.pid, self.ppid) == (other.pid, other.ppid)

    def __hash__(self):
        return hash((self.pid, self.ppid))


@dataclass(eq=False, frozen=True)
class ExecutedCommand(ObservedProcess):
    """
    The following class is used to store information about directly executed processes, and includes
    the stodut, and stderr associated with a given invocation as well as the process' exit status.
    """
    stdout: str = field(repr=False)
    stderr: str = field(repr=False)
    exit_status: int = 0

    def __iter__(self):
        for child_process in self.child_processes:
            yield child_process


def execute_command(command, command_type=DEFAULT_COMMAND_TYPE, timeout=DEFAULT_COMMAND_TIMEOUT):
    """
    Executes the provided command.

    :param command: a command (e.g. 'ls -lah').
    :param command_type: a command type (e.g.
    :param timeout: an integer, or float representing how long to wait for the process to exit
        before timing out.

    :return: information about the executed process.
    """
    command_type = command_type or DEFAULT_COMMAND_TYPE
    logger.info("Executing %s command: '%s' (timeout: %s)", command_type, command, timeout or None)

    #: FileNotFoundError will be raised if we couldn't find the corresponding command launcher.
    try:
        result = _execute_command(command, command_type, timeout)
    except FileNotFoundError as exception:
        logger.error("Failed to execute %s command: '%s' - %s", command_type, command, exception)
    else:
        logger.info(
            "Successfully executed %s command: '%s' (PID: %s, PPID: %s, exit status: %s)",
            command_type, command, result.pid, result.ppid, result.exit_status
        )
        return result


def _execute_command(command, command_type=DEFAULT_COMMAND_TYPE, timeout=DEFAULT_COMMAND_TIMEOUT):

    #: Validate the provided command.
    command = ensure_type(command, str)

    #: Validate the provided command timeout.
    timeout = ensure_type(timeout, (int, float, None))
    if timeout is not None and timeout < 0:
        raise ValueError("Timeout must be non-negative: {}".format(timeout))

    #: Validate the provided command type.
    command_type = command_type or DEFAULT_COMMAND_TYPE
    if command_type not in SUPPORTED_COMMAND_TYPES:
        raise ValueError("Unsupported command type: {} (supported: {})".format(
            command_type, SUPPORTED_COMMAND_TYPES
        ))

    #: Use a launcher to execute the provided command (e.g. bash -c 'ls -lah').
    launcher = COMMAND_TYPES_TO_COMMAND_LAUNCHERS[command_type]

    cwd = os.getcwd()
    ppid = os.getpid()
    start_timestamp = time.time()
    with subprocess.Popen(
            args=launcher + [command],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
            env=os.environ
    ) as popen:
        pid = popen.pid

        #: Wait a few milliseconds before performing context gathering (race between fork/exec()).
        if hodgepodge.helpers.platform_is_posix():
            time.sleep(0.01)

        #: Perform secondary context gathering.
        name = None
        executable_path = None
        command_line = None

        try:
            process_handle = psutil.Process(popen.pid)
            with process_handle.oneshot():
                name = process_handle.name()
                executable_path = process_handle.exe()
                command_line = ' '.join(process_handle.cmdline())
                cwd = process_handle.cwd()

        except (psutil.NoSuchProcess, psutil.AccessDenied) as exception:
            logger.warning(
                "Failed to gather process context (PID: %s, PPID: %s): %s",
                pid, ppid, exception
            )

        #: Wait for the process to exit.
        try:
            stdout, stderr = popen.communicate(timeout=timeout)
        except TimeoutExpired:
            popen.kill()
            stdout, stderr = popen.communicate()
        except Exception:
            popen.kill()
            raise

        #: Wait for the process to complete (reaps the dead process on POSIX).
        popen.wait()

        #: Gather additional information, such as the exit status, stdout, and stderr.
        exit_status = popen.poll()
        stdout = hodgepodge.helpers.bytes_to_str(stdout)
        stderr = hodgepodge.helpers.bytes_to_str(stderr)

        return ExecutedCommand(
            pid=pid,
            ppid=ppid,
            cwd=cwd,
            command_line=command_line,
            name=name,
            executable_path=executable_path,
            start_timestamp=start_timestamp,
            stdout=stdout,
            stderr=stderr,
            exit_status=exit_status,
            child_processes=[],
        )


def terminate_process(pid, include_children=True):
    """
    Terminates the process with the provided PID.

    :param pid: a PID.
    :param include_children: whether or not to recursively kill subprocesses.
    """
    logger.warning("Terminating process (PID: %s)", pid)
    try:
        process = psutil.Process(pid)
        if include_children:
            for child in process.children(recursive=True):
                child.kill()
        process.kill()
    except psutil.NoSuchProcess:
        pass
    except OSError:
        logger.error("Failed to terminate process (PID: %s)", pid)


def get_executable_path(command):
    """
    Looks up the name of the executable associated with the provided command.

    :param command: a command string (e.g. 'ls -lah').
    :return: the name of the executable (e.g. '/bin/ls').
    """
    command = command.split()[0] if ensure_type(command, str) else command

    #: Look for the specified executable on the ${PATH}.
    executable = distutils.spawn.find_executable(command)
    if executable:
        return executable

    #: Use the `where` or `which` command to lookup the path of the executable.
    if hodgepodge.helpers.platform_is_windows():
        locator_command = "where {}".format(command)
    else:
        locator_command = "which {}".format(command)

    result = execute_command(locator_command)
    path = None
    if result and result.exit_status == 0:
        executable = result.stdout.strip()
        if os.path.exists(executable):
            path = executable
    return path


def get_executable_name(command):
    """
    Looks up the name of the executable associated with the provided command.

    :param command: a command string (e.g. 'ls -lah').
    :return: the name of the executable (e.g. 'ls').
    """
    executable_path = get_executable_path(command)
    if executable_path:
        executable_path = hodgepodge.path.basename(executable_path)
    return executable_path
