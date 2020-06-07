from rich.console import Console
from rich.table import Table


def print_params(params: dict):
    table = Table(title='Training Config')

    table.add_column("Parameter")
    table.add_column("Value", justify='right', style='green')

    for i in params.keys():
        table.add_row(i, str(params[i]))

    console = Console()
    console.print(table)
