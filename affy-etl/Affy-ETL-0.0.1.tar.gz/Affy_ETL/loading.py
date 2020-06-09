import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.types import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
import pandas as pd

def loading(user , passwd, address, dbname, tablename):
    db_connect = "mysql+pymysql://{}:{}@{}/{}".format(user, passwd, address, dbname)
    engine = sqlalchemy.create_engine(db_connect, encoding='utf8', echo=True)
    con = engine.connect()

    pandas_df.to_sql(tablename, engine, schema=dbname, if_exists='append', index=False)

    # Alter ID type
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    sql_alter_idtype = "ALTER TABLE {} COLUMN ID varchar(128);".format(tablename)
    session.execute(sql_alter_idtype)
    # Alter ID to PK
    sql_alter_idkey = "ALTER TABLE {} ADD PRIMARY KEY (ID);".format(tablename)
    session.execute(sql_alter_idkey)
    # session.execute("ALTER TABLE {} DROP PRIMARY KEY;".format(tablename))
    con.close()