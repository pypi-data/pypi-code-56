from typing import List

from git import Commit
from rich import print
from rich.console import Console
from rich.table import Table

from we_are_venom.common_types import ModuleAccumulation


def output_accumulation_table(module_accumulation_info: List[ModuleAccumulation]) -> None:
    is_accumulated_map = {
        None: '-',
        True: '✅',
        False: '❌',
    }
    console = Console()
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('Module', style='dim')
    table.add_column('Total lines')
    table.add_column('Touched lines')
    table.add_column('Accumulated')
    for module_info in module_accumulation_info:
        table.add_row(
            module_info.module_name,
            str(module_info.total_lines),
            str(module_info.touched_lines),
            is_accumulated_map[module_info.is_accumulated],
        )
    console.print(table)


def output_commits(commits: List[Commit]) -> None:
    console = Console()
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('Commit hash', style='dim')
    table.add_column('Summary')
    table.add_column('Commit datetime')
    for commit in commits:
        table.add_row(
            commit.hexsha,
            commit.summary,
            str(commit.committed_datetime),
        )
    console.print(table)
    print(f'[bold]Total {len(commits)} commits[/bold]')  # noqa: T001
