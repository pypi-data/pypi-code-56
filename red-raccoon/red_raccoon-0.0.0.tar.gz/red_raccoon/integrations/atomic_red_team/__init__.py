
import os

#: Look for the atomic-red-team directory in the same directory as the red-raccoon repository.
DEFAULT_ATOMIC_RED_TEAM_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "../../../../atomic-red-team"
)

DEFAULT_COMMAND_TIMEOUT = 5
DEFAULT_COMMAND_TIMEOUT_FOR_DEPENDENCY_RESOLUTION = 60
