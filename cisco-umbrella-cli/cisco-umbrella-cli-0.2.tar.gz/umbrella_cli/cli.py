import os

import requests
import click
from requests.auth import HTTPBasicAuth

from umbrella_cli import commands

requests.urllib3.disable_warnings() #? Disable HTTPS warnings for requests


@click.group(name="umbrella-cli")
@click.option("--access", prompt="Enter your API Access key", help="Umbrella API Access Key")
@click.option("--secret", prompt="Enter your API Secret key", hide_input=True, help="Umbrella API Secret Key")
@click.option("--org", prompt="Enter your organization ID", help="Umbrella Organizaton ID")
@click.pass_context
def cli(ctx, access, secret, org):
    ctx.ensure_object(dict)

    ctx.obj['ACCESS'] = access
    ctx.obj['SECRET'] = secret
    ctx.obj['ORG'] = org


#? Adding commands to group
cli.add_command(commands.sites)
cli.add_command(commands.internal_networks)


if __name__ == "__main__":
    cli(obj={}) # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
