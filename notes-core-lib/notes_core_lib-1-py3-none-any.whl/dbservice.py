from . import connection as con
import psycopg2

connectionFactory = con.Connection()

def set_config_path(path):
    connectionFactory.set_path(path)

def _get_connection():
    return connectionFactory.make_connection()

def _get_cursor():
    return _get_connection().cursor()

def select_one(query, params):
    cur = _get_cursor()
    cur.execute(query, params)
    return cur.fetchone()

def select_all(query):
    cur = _get_cursor()
    cur.execute(query)
    return cur.fetchall()

def execute(statement, params):
    cur = _get_cursor()
    cur.execute(statement, params)

def execute_with_return(statement, params):
    cur = _get_cursor()
    cur.execute(statement, params)
    return cur.fetchone()[0]

def commit():
    connectionFactory.get_connection().commit()
