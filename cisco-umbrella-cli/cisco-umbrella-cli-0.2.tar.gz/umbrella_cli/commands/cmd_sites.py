"""
    This module contains the sub-commands of umbrella sites.
"""

import click
import requests
from requests.auth import HTTPBasicAuth

from umbrella_cli import services
from umbrella_cli.models import Site

@click.group(name="sites")
@click.pass_context
def sites(ctx):
    pass


@sites.command(name="list")
@click.pass_context
def get_all(ctx):
    """ Get the list of sites """
    api = services.SitesEndpointService(
        access=ctx.obj["ACCESS"], 
        secret=ctx.obj["SECRET"], 
        org_id=ctx.obj["ORG"]
    )
    
    try:
        sites = api.get_list()

        click.echo((
            "+===============================================+"
            "|+++ Umbrella Sites for Organization {org} +++|"
            "|===============================================|"
            "| Site ID | Name                                |"
            "|-----------------------------------------------|"
        ).format(org=ctx.obj['ORG'])
        )
        for site in sites:
            click.echo("| {:8}| {:36}|".format(str(site.site_id), site.name))
        
        click.echo("+===============================================+")

    except Exception as error:
        click.secho(str(error), fg="red")

@sites.command()
@click.argument("name")
@click.pass_context
def create(ctx, name):
    """ Create a new site """
    api = services.SitesEndpointService(
        access=ctx.obj["ACCESS"], 
        secret=ctx.obj["SECRET"], 
        org_id=ctx.obj["ORG"]
    )

    try:
        site = Site(name)

        result = api.create(site)

        click.secho("New site created with ID {id}".format(id=result.site_id),
                    fg="green")
    except Exception as error:
        click.secho(str(error), fg="red")
    

@sites.command(name="import")
@click.argument("filepath")
@click.pass_context
def bulk_import(ctx, filepath):
    """Import a set of sites based on a backend provider.

    Args:
        ctx (CLick Context): Click context
        filepath (FileHandler): File handler for CSV ?* to change
    """

    api = services.SitesEndpointService(
        access=ctx.obj["ACCESS"], 
        secret=ctx.obj["SECRET"], 
        org_id=ctx.obj["ORG"]
    )

    try:
        csv_service = services.InternalNetworkCsvService(filepath)

        sites_to_import = csv_service.sites()
        existing_sites = api.get_list()

        new_sites_created = []

        click.secho(
            f"{str(len(sites_to_import))} to import from list",
            fg="green"
        )

        for site in sites_to_import:
            if not [existing_site for existing_site in existing_sites \
                    if existing_site.name == site.name]:
                click.echo(
                    f"-> Creating new site with name {site.name}"
                )
                new_sites_created.append(api.create(site))

        click.secho(
            f"Created a total of {str(len(new_sites_created))} site(s)",
            fg="green"
        )

    except Exception as e:
        click.secho(str(e), fg="red")