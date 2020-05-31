"""Outcome module for CLI.

  Typical usage example:

  outcome_command = OutcomeCommand()
  outcome_command.run()
"""
import time
from argparse import ArgumentParser, Namespace
from timeit import default_timer

from nwa.cli.base_command import BaseCommand
from nwa.logger import LOGGER


class OutcomeCommand(BaseCommand):
    """Initialise outcome command.

    Example:
        nwa outcome -f <json_file>
    """

    def __init__(self):
        super(OutcomeCommand, self).__init__()
        self.name = "outcome"

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-f", "--file", required=True, help="The json file of the graph",
        )

        parser.add_argument(
            "-o",
            "--output",
            required=False,
            default=time.strftime("%Y%m%d-%H%M%S"),
            help="The filename to use as the output file",
        )

    def validate_args(self, args: Namespace) -> None:
        """Check command given argument, file.

        Requires a non-empty file.

        Raises:
            Exception: If file is not valid.
        """
        return

    def execute(self, args: Namespace) -> None:
        start_time = default_timer()
        self.analyse(args.file, args.output)
        elapsed_time = default_timer() - start_time
        LOGGER.debug(f'Command "{self.name}" took {elapsed_time:.2f} seconds.')

    def analyse(self, file: str = "", output: str = "") -> None:
        """Calls the outcome analysis with the provided graph data.

        Execute analysis, write output.

        Args:
            file: The graph file for the input of the command.
            output: The filename for the output of the command.
        """
        raise NotImplementedError(
            f"Method: analyse is undefined for command {self.name}"
        )
