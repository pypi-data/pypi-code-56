import os

#: Look for the atomic-red-team directory in the same directory as the red-raccoon repository.
DEFAULT_ATOMIC_RED_TEAM_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "../../../atomic-red-team"
)

#: Default command timeouts.
DEFAULT_COMMAND_TIMEOUT = 15

#: Define a set of recommended disruptive command exclusions.
RECOMMENDED_DISRUPTIVE_COMMAND_EXCLUSIONS = {
    '*shutdown*',
    'rm -rf /',
    'rd/s/q/ C:\\',
    'C:\\boot.ini',
    'C:\\ntldr',
    'C:\\Windows\\win.ini',
    'reg delete HKCR/.exe',
    'reg delete HKCR/.dll',
    'reg delete HKCR/*',
    'delete %systemdrive%',
}
