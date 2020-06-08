
import click
import subprocess


@click.command()
@click.argument('args', nargs=-1)
def cli(args):
    assert len(args) == 2
    print(args)
    command = f'diff -u {args[0]} {args[1]} | ydiff -s -w 0'
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    cli()
