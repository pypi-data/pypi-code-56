"""
Main module for textwarden.
"""
from textwarden import commands
from textwarden import config
from textwarden import tools
import asyncio
import click
import discord
import textwarden
import logging

logger = logging.getLogger(__name__)
client = discord.Client()

@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
    logger.debug('msg|{}: {}'.format(msg.author, msg.content))
    if msg.author == client.user:
        return
    if msg.content.startswith(config.prompt):
        command, _ = tools.cmd_arg_split(msg)
        cmd_function = None
        response = None
        try:
            cmd_function = getattr(commands, command)
        except AttributeError as e:
            pass
        if cmd_function:
            response = cmd_function(msg)
        else:
            response = "‼️ Unknown command."
        await msg.channel.send(response)

@click.group()
@click.version_option(version=textwarden.__version__,
    message="%(prog)s %(version)s - {}".format(textwarden.__copyright__))
@click.option('-d', '--debug', is_flag=True,
    help="Enable debug mode with output of each action in the log.")
@click.option('--log', type=str)
@click.pass_context
def cli(ctx, log, **kwargs): # pragma: no cover
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)03d, %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = log,
        level = logging.DEBUG if ctx.params.get('debug') else logging.INFO,
        )

@cli.command()
@click.argument('distoken')
@click.option('--dev', type=str, multiple=True,
    help="Developer uuid. Can be used multiple times.")
def run(distoken, dev, **kwargs): # pragma: no cover
    "Run on discord."
    config.devs.extend(dev)
    client.run(distoken)

if __name__ == '__main__': # pragma: no cover
    cli()

