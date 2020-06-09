"""CLI - Command Line Interface"""
import click


@click.command()
def main():
    click.echo("Hello, World!")
