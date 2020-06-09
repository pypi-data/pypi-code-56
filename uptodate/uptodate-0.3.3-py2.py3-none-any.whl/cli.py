import typer

from pathlib import Path
from typing import List

try:
    from uptodate.core import UpToDate
except Exception:
    from core import UpToDate  # type: ignore


def up_to_date(file_paths: List[Path] = typer.Argument(None, exists=True)):
    """Scan requirements.txt file for dependences which are not up to date"""

    uptodate = UpToDate()
    uptodate.run(file_paths)


def main():
    typer.run(up_to_date)


if __name__ == '__main__':
    main()
