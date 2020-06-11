import sys
from collections import OrderedDict
from knack import CLI, CLICommandsLoader, ArgumentsContext
from knack.commands import CommandGroup
from knack.help import CLIHelp

import phoenix.cli.commands.data_help

WELCOME_MESSAGE = r"""
  ______ _                      ___   __
 | ___ \ |                    (_) \ / /
 | |_/ / |__   ___   ___ _ __  _ \ V /
 |  __/| '_ \ / _ \ / _ \ '_ \| |/   \
 | |   | | | | (_) |  __/ | | | / /^\ \
 \_|   |_| |_|\___/ \___|_| |_|_\/   \/

"""


class PxCLIHelp(CLIHelp):
    def __init__(self, cli_ctx=None):
        super(PxCLIHelp, self).__init__(
            cli_ctx=cli_ctx,
            privacy_statement="My privacy statement.",
            welcome_message=WELCOME_MESSAGE,
        )


class PxCliCommandLoader(CLICommandsLoader):
    def load_command_table(self, args):
        with CommandGroup(self, "data", "phoenix.cli.commands.data#{}") as g:
            g.command("ingest", "ingest", is_preview=True)

        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        with ArgumentsContext(self, "data") as ac:
            ac.argument("read_buffer_size", type=int, is_experimental=True)
        super(PxCliCommandLoader, self).load_arguments(command)
