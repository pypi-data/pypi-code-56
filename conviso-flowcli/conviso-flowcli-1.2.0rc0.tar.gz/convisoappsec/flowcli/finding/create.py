import click

from convisoappsec.flow.version_control_system_adapter import GitAdapter
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option


@click.command()
@click.argument("project-code", required=True)
@click.argument("finding-file", nargs=-1, required=True,  type=click.File('r'))
@click.option(
    '-c',
    '--current-commit',
    required=False,
    help='The hash of current commit. If no value is set so the HEAD commit will be used.',
)
@click.option(
    "-r",
    "--repository-dir",
    required=False,
    type=click.Path(exists=True),
    default=".",
    show_default=True,
    help='The root dir of repository.',
)
@help_option
@pass_flow_context
def create(flow_context, project_code, finding_file, repository_dir, current_commit):
    try:
        git = GitAdapter(repository_dir)
        current_commit = current_commit or git.head_commit
        commit_refs = git.show_commit_refs(current_commit)

        flow = flow_context.create_flow_api_client()
        flow.findings.create(project_code, commit_refs, finding_file)
    except Exception as e:
        raise click.ClickException(str(e)) from e

