import click
from fauxcyrillic import utils


@click.command()
@click.argument('text', default='', type=str)
def main(text):
    """Converts user input to faux Cyrillic characters"""
    if text == '':
        text = click.prompt('Please enter a string to convert', type=str)
    click.echo(utils.convert(text))
