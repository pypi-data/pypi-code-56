import os

from click import group, option, argument, Path, echo
from rich import print

from we_are_venom.utils.accumulation import (
    calclulate_module_accumulation_info,
    calculate_total_accumulation_percent,
)
from we_are_venom.utils.config import load_config_from
from we_are_venom.utils.git import fetch_git_history
from we_are_venom.utils.output import output_accumulation_table, output_commits


@group()
def cli() -> None:
    pass


@cli.command()
@argument('email')
@argument('path', type=Path(exists=True, file_okay=False, resolve_path=True))
@option('--verbose', is_flag=True, default=False)
@option('--config_file_name', default='setup.cfg')
@option('--config_file_path', type=Path(exists=True, dir_okay=False, resolve_path=True))
def check(
    email: str,
    path: str,
    verbose: bool,
    config_file_name: str,
    config_file_path: str,
) -> None:
    if not os.path.exists(os.path.join(path, '.git')):
        echo(f'{path} is not git root.', err=True)
        return

    config_path = config_file_path or os.path.join(path, config_file_name)
    if not os.path.exists(config_path):
        echo(f'{config_path} does not exists. Please, provide venom config as docs says.')

    config = load_config_from(config_path)
    if not config:
        echo(f'Error loading config from {config_path}.', err=True)
        return

    raw_git_history = fetch_git_history(path, email, config)
    if verbose:
        output_commits(raw_git_history)
    module_accumulation_info = calclulate_module_accumulation_info(raw_git_history, email, config)
    total_accumulation_percent = calculate_total_accumulation_percent(module_accumulation_info)
    output_accumulation_table(module_accumulation_info)
    print(f'[bold]Total accumulation rate: {total_accumulation_percent}%[/bold]')  # noqa: T001


if __name__ == '__main__':
    cli()
