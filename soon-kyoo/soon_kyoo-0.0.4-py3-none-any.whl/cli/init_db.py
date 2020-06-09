"""Functionality for initializing the database.

Click commands:
init_db
"""

import sqlite3

import click

from soon_kyoo.config import db_path, schema


@click.command()
def init_db():
    db_path.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(str(db_path))
    # Create tables.
    for table_name, table_info in schema.items():
        sql_str = f"CREATE TABLE {table_name} (" \
            + ', '.join([f"{col_name} {col_descr}"
                for col_name, col_descr in table_info.items()]) \
            + ')'
        try:
            with con:
                con.execute(sql_str)
            click.echo(f'Table {table_name!r} created')
        except sqlite3.OperationalError:
            click.echo(f'Table {table_name!r} already exists')
    # Close database connection.
    con.close()
    click.echo('Database initialized')
