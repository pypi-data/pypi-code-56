from red_raccoon.cli.atomic_red_team import atomic_red_team
from red_raccoon.cli.stix import stix
from red_raccoon.cli.mitre_attack import mitre_attack
from red_raccoon.cli.mitre_attack_enterprise import mitre_attack_enterprise
from red_raccoon.cli.mitre_attack_mobile import mitre_attack_mobile
from red_raccoon.cli.mitre_attack_pre_attack import mitre_attack_pre_attack
from red_raccoon.cli.mitre_attack_evaluations import mitre_attack_evaluations
from red_raccoon.cli.mitre_attack_navigator import mitre_attack_navigator
from red_raccoon.cli.windows_defender_atp import windows_defender_atp
from red_raccoon.cli.commands import commands
from red_raccoon.cli.files import files

import logging
import click


@click.group()
def cli():
    pass


if __name__ == "__main__":
    def main():
        logging.basicConfig(level=logging.INFO)

        groups = [
            atomic_red_team,
            stix,
            mitre_attack,
            mitre_attack_enterprise,
            mitre_attack_mobile,
            mitre_attack_pre_attack,
            mitre_attack_navigator,
            mitre_attack_evaluations,
            windows_defender_atp,
            commands,
            files,
        ]
        for group in groups:
            cli.add_command(group)
        cli()
    main()
