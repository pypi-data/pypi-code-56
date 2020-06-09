import click

from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli import common


@click.command()
@help_option
@click.argument("project-code", required=True)
@click.argument("current-tag", required=True)
@click.argument("previous-tag", required=False)
@pass_flow_context
def values(flow_context, current_tag, previous_tag, project_code):
    try:
        flow = flow_context.create_flow_api_client()
        deploy = flow.deploys.create(project_code, current_tag, previous_tag)
        common.notify_created_deploy(deploy)
    except Exception as e:
        raise click.ClickException(str(e)) from e