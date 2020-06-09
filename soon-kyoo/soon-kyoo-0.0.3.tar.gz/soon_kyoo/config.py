"""Configuration variables.
"""

from collections import OrderedDict as ODict
import pathlib


# Database location.
here = pathlib.Path(__file__)
db_path = here.parents[0] / 'instance' / 'queue.sqlite'

# Database schema.
# NOTE: Changing this configuration will not change the database schema.
# In order to do so, the database must be re-initialized.
schema = ODict(
    queue=ODict(
        task_id='TEXT PRIMARY KEY NOT NULL',
        queue_name='TEXT',
        position='INTEGER UNIQUE NOT NULL',
        published='TIMESTAMP NOT NULL',
        args='TEXT',
        kwargs='TEXT',
    ),
    work=ODict(
        task_id='TEXT PRIMARY KEY NOT NULL',
        queue_name='TEXT',
        started='TIMESTAMP NOT NULL',
        status='TEXT',
    ),
)
