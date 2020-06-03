import click

@click.group()
def cli():
    pass

@click.command()
def init():
    click.echo('CLI tools coming soon.')

cli.add_command(init)