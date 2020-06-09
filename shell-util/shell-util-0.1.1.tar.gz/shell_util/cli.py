# from pathlib import Path

import click
from shell_util import shell
import subprocess


@click.group()
def cli():
    return True


@cli.command()
@click.argument('command_args', nargs=-1)
def run_command(command_args):

    # print('[START]')
    command = ' '.join(command_args)
    # print(command)
    # result = shell.run_command(command)

    # status, output = subprocess.getstatusoutput('ls')
    result = shell.run_command(command)
    # import pdb; pdb.set_trace()

    # print('[END]')


if __name__ == '__main__':
    cli()
