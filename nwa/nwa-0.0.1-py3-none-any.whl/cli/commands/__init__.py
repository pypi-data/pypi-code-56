"""Commands init
"""
from nwa.cli.commands.controllability import ControllabilityCommand
from nwa.cli.commands.intervention import InterventionCommand
from nwa.cli.commands.network import NetworkCommand
from nwa.cli.commands.outcome import OutcomeCommand
from nwa.cli.commands.xcs import XcsCommand

COMMANDS = [
    ControllabilityCommand,
    InterventionCommand,
    NetworkCommand,
    OutcomeCommand,
    XcsCommand,
]
