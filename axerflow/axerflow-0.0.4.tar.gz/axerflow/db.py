import click

import axerflow.store.db.utils


@click.group("db")
def commands():
    """
    Commands for managing an Axerflow tracking database.
    """
    pass


@commands.command()
@click.argument("url")
def upgrade(url):
    """
    Upgrade the schema of an Axerflow tracking database to the latest supported version.

    **IMPORTANT**: Schema migrations can be slow and are not guaranteed to be transactional -
    **always take a backup of your database before running migrations**. The migrations README,
    which is located at
    https://github.com/axerflow/axerflow/blob/master/axerflow/store/db_migrations/README.md, describes
    large migrations and includes information about how to estimate their performance and
    recover from failures.
    """
    engine = axerflow.store.db.utils.create_sqlalchemy_engine(url)
    if axerflow.store.db.utils._is_initialized_before_axerflow_1(engine):
        axerflow.store.db.utils._upgrade_db_initialized_before_axerflow_1(engine)
    axerflow.store.db.utils._upgrade_db(engine)
