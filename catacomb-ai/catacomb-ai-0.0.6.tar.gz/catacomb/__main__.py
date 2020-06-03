import click

@click.group()
def cli():
    click.echo("Welcome to Catacomb!")

@click.command()
def init():
    click.echo("CLI tools coming soon!")

if __name__ == '__main__':
    cli()