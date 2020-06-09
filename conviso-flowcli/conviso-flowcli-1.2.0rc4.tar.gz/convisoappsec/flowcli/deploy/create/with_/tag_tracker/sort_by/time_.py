import click

from convisoappsec.flow import api
from convisoappsec.flow.version_searchers import TimeBasedVersionSearcher
from convisoappsec.flow.version_control_system_adapter import GitAdapter
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli import common

from convisoappsec.flowcli.deploy.create.with_.tag_tracker.context import (
    pass_tag_tracker_context
)


@click.command('time')
@help_option
@click.argument("project-code", required=True)
@pass_tag_tracker_context
@pass_flow_context
def time_(flow_context, tag_tracker_context, project_code):
    try:
        repository_dir = tag_tracker_context.repository_dir
        git_adapter = GitAdapter(repository_dir)

        version_searcher = TimeBasedVersionSearcher(
            git_adapter
        )

        result = version_searcher.find_current_and_previous_version()

        flow = flow_context.create_flow_api_client()

        deploy = flow.deploys.create(
            project_code,
            result.current_version,
            result.previous_version,
            diff_content=git_adapter.diff(
                result.previous_version, result.current_version,
            )
        )

        common.notify_created_deploy(deploy)
    except Exception as e:
        raise click.ClickException(str(e)) from e
