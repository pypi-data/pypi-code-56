# Python to R
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
import os
# Loading to MySQL
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.types import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
import pandas as pd

def extract(dir, cdf = "hgu133plus2cdf"):
    affy = importr('affy')
    annotation = importr(cdf)
    print("Annotation is using {}".format(annotation))

    os.chdir(dir)
    datapath = os.getcwd()
    datalist = [i for i in os.listdir(datapath) if i.endswith(".CEL")]
    print("Catch CEL data {}".format(datalist))

    cdatalist = robjects.r['as.character'](datalist)
    rawdata = affy.ReadAffy(filenames=cdatalist)
    rmdata = affy.rma(rawdata)

    data = robjects.r['exprs'](rmdata)
    df = robjects.r['data.frame'](data)

    rID_list = robjects.r['rownames'](df)
    df_len = len(rID_list)
    print("This Platform have {} probes".format(df_len))

    return df, df_len


def transform(df, df_len):
    pandas2ri.activate()
    r.data('df')
    pandas_df = df.head(df_len)

    col_name = pandas_df.columns.to_list()
    col_name.insert(0, "ID")
    Inputid = pandas_df.index
    pandas_df.reindex(columns=col_name)
    pandas_df["ID"] = Inputid
    pandas_df = pandas_df.reindex(columns=col_name)

    return pandas_df


def loading(user, passwd, address, dbname, tablename, data):
    try:
        db_connect = "mysql+pymysql://{}:{}@{}/{}".format(user, passwd, address, dbname)
        engine = sqlalchemy.create_engine(db_connect, encoding='utf8', echo=True)
        con = engine.connect()

        pandas_df = data
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

        return "Loading Success"
    except:
        return  "Loading Failed"