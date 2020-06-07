"""
Set of SQLAlchemy database schemas supported in Axerflow for tracking server backends.
"""

POSTGRES = 'postgresql'
MYSQL = 'mysql'
SQLITE = 'sqlite'
MSSQL = 'mssql'

DATABASE_ENGINES = [
    POSTGRES,
    MYSQL,
    SQLITE,
    MSSQL
]
