import os
import requests

from collections import namedtuple
from typing import List, Dict
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.padding import Padding

Row = namedtuple('Row', ['name', 'current_version', 'latest_version'])

console = Console()


class UpToDate:
    DEFAULT_FILE_PATH = Path('requirements.txt')

    def __init__(self) -> None:
        self.scanner = RequirementsScanner()
        self.pypi = PyPI()

    def run(self, file_paths: List[Path]):
        if not file_paths:
            if os.path.isfile(self.DEFAULT_FILE_PATH):
                self._check_file(self.DEFAULT_FILE_PATH)
            else:
                console.print('No requirements file found', style='yellow')
        else:
            self._check_files(file_paths)

    def _check_files(self, file_paths: List[Path]) -> None:
        for file_path in file_paths:
            self._check_file(file_path)

    def _check_file(self, file_path: Path) -> None:
        console.print(file_path, style='blue')
        dependences = self.scanner.get_dependences(file_path)
        versions = self.pypi.get_latest_versions(list(dependences.keys()))
        rows = self._prepare_rows(dependences, versions)
        if len(rows) == 0:
            console.print(
                Padding('Everything is up to date', (0, 0, 1, 2)), style='green'
            )
        else:
            self._draw_table(rows)

    def _prepare_rows(
        self, dependences: Dict[str, str], latest_versions: Dict[str, str]
    ) -> List[Row]:
        return [
            Row(
                name=name,
                current_version=current_version,
                latest_version=latest_versions[name],
            )
            for name, current_version in dependences.items()
            if current_version != latest_versions[name]
        ]

    def _draw_table(self, rows: List[Row]) -> None:
        table = Table(show_header=True, header_style='bold cyan')
        table.add_column('Name', style='dim', justify='left')
        table.add_column('Current', justify='center')
        table.add_column('Latest', justify='center')

        for row in rows:
            table.add_row(row.name, row.current_version, row.latest_version)

        console.print(Padding(table, (0, 0, 1, 2)))


class RequirementsScanner:
    def get_dependences(self, file_path: Path) -> Dict[str, str]:
        dependences = {}

        with open(file_path, 'r') as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                if not self._is_supported(line):
                    console.print(
                        Padding('SKIPPED: {}'.format(line), (0, 0, 0, 2)),
                        style='yellow',
                    )
                    continue

                name, version = line.strip().split('==')
                dependences[name] = version

        return dependences

    def _is_supported(self, line: str) -> bool:
        if '==' not in line:
            return False
        if '[' in line and ']' in line:
            return False

        return True


class PyPI:
    URL_PATTERN = 'https://pypi.org/pypi/{}/json'
    PROGRESS_BAR_THRESHOLD = 10

    def get_latest_versions(self, dependences: List[str]) -> Dict[str, str]:
        versions = {}

        for dependence in self._warp(dependences):
            url = self.URL_PATTERN.format(dependence)
            response = requests.get(url)
            data = response.json()
            latest_version = data['info']['version']
            versions[dependence] = latest_version

        return versions

    def _warp(self, dependences: List[str]):
        if len(dependences) >= self.PROGRESS_BAR_THRESHOLD:
            return track(dependences, description='Checking...')

        return dependences
