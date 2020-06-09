import click

@click.group()
def cli():
    pass

@cli.command()
def upload():
    click.echo("upload here")

if __name__ == "__main__":
    cli()
