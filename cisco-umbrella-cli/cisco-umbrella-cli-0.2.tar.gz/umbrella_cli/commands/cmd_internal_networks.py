"""
    This module contains the sub-commands of umbrella internal networks.
"""

import click
import requests
from requests.auth import HTTPBasicAuth

from umbrella_cli import services
from umbrella_cli.models import InternalNetwork, Site


@click.group(name="internal-networks")
@click.pass_context
def internal_networks(ctx):
    pass


@internal_networks.command(name="list")
@click.pass_context
def get_all(ctx):
    """ Get the list of internal networks """
    api = services.InternalNetworkEndpointService(
        access=ctx.obj["ACCESS"],
        secret=ctx.obj["SECRET"],
        org_id=ctx.obj["ORG"]
    )

    try:
        internal_networks = api.get_list()

        click.echo((
            "+====================================================+\n"
            "|+++         Umbrella Internal networks for       +++|\n"
            f"|+++            Organization {api.org_id:8}      +++|\n"
            "|====================================================|\n"
            "| IP Address         | Name                          |\n"
            "|----------------------------------------------------|"
        ))

        for network in internal_networks:
            address = f"{network.ip_address}/{network.prefix_length}"
            click.echo((
                f"| {address:18} "
                f"| {network.name:29} |"
            ))
        
        click.echo("+====================================================+")
    except Exception as error:
        click.secho(str(error), fg="red")


@internal_networks.command(name="import")
@click.argument("filepath")
@click.pass_context
def bulk_import(ctx, filepath):
    api = services.InternalNetworkEndpointService(
        access=ctx.obj["ACCESS"],
        secret=ctx.obj["SECRET"],
        org_id=ctx.obj["ORG"]
    )

    sites_api = services.SitesEndpointService(
        access=ctx.obj["ACCESS"],
        secret=ctx.obj["SECRET"],
        org_id=ctx.obj["ORG"]
    )

    try:
        existing_networks = api.get_list()
        sites = sites_api.get_list()

        csv_service = services.InternalNetworkCsvService(filepath)

        networks_to_import = csv_service.internal_networks()

        click.secho(
            f"{str(len(networks_to_import))} networks found in provider"
        )

        new_networks_created = []

        for internal_network in networks_to_import:
            if not [network for network in existing_networks \
                    if network.name == internal_network.name]:
                site = [site for site in sites if site.name == internal_network.site_name]
                
                if site:
                    site = site[0]
                else:
                    click.secho(
                        f"---> The related site {internal_network.site_name} doesn't exist, creating it",
                        fg="yellow"
                    )
                    site = sites_api.create(
                            Site(name=internal_network.site_name)
                        )
                    sites.append(site)

                    click.secho(
                        f"------> Creating new site with name {site.name}",
                        fg="green"
                    )
                        
                click.secho(
                    f"-> Creating network {internal_network.name}({internal_network.ip_address}/{str(internal_network.prefix_length)})"
                )

                if site:
                    internal_network.site_id = site.site_id

                new_networks_created.append(api.create(internal_network))
            else:
                click.secho(
                    f"-> Skipping network {internal_network.name}({internal_network.ip_address}/{str(internal_network.prefix_length)})"
                )
        click.secho(
            f"Created a total of {str(len(new_networks_created))} network(s)",
            fg="green"
        )
                   

    except Exception as error:
        click.secho(str(error), fg="red")