"""
Database connection.
"""
from textwarden import config
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)

CREATE_TABLES=[
    '''
    CREATE TABLE IF NOT EXISTS users (
        uuid TEXT NOT NULL PRIMARY KEY,
        data BLOB NOT NULL
        );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS configs (
        server TEXT NOT NULL PRIMARY KEY,
        data BLOB NOT NULL
        )
    '''
]

def execute(query, args=[]):
    "Execute a query on the database."
    db_path = os.path.expanduser(config.db_path)
    if not os.path.isdir(os.path.dirname(db_path)):
        db_dir = os.path.dirname(db_path)
        logger.info("Creating database directory '{}'.".format(db_dir))
        os.makedirs(db_dir)
    if not os.path.isfile(db_path):
        logger.info("Initiating sqlite3 database in '{}'.".format(db_path))
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            for sql in CREATE_TABLES:
                cur.execute(sql)
    data = None
    with sqlite3.connect(db_path) as con:
        con.set_trace_callback(logger.info)
        cur = con.cursor()
        cur.execute(query, args)
        data = cur.fetchall()
    #return { 'data':data, 'count':cur.rowcount }
    return data

