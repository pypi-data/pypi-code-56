import pymysql as pq
import os

MYSQL_IP = os.getenv('MYSQL_IP', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))


class Mysql(object):
    def __init__(self, user="docker", passwd="123456", db="docker", charset='utf8mb4'):
        # connect database with pymysql
        print("Start conneting mysql...")
        print("Host:%s, Port:%d" % (MYSQL_IP, MYSQL_PORT))
        try:
            self.__conn__ = pq.connect(host=MYSQL_IP, port=MYSQL_PORT, user=user,
                                       passwd=passwd, db=db, charset=charset)
            self.__cursor__ = self.__conn__.cursor()
            print("Connected! ")
        except pq.err.OperationalError as e:
            self.__conn__, self.__cur__ = None, None
            print(e)

    def cursor(self):
        return self.__cur__;

    def insert(self, table_name, col_names, value=None):
        placeholder = ",".join(["%s"] * len(col_names))
        if type(col_names) == list or type(col_names) == tuple:
            col_names = ','.join(map(lambda x: "`%s`" % x, col_names))
        elif type(col_names) == dict:
            value = tuple(col_names.values())
            col_names = ','.join(map(lambda x: "`%s`" % x, list(col_names.keys())))
        sql = "insert into %s(%s) values (%s)" % (table_name, col_names, placeholder)
        self.__cursor__.execute(sql, value)
        self.__conn__.commit()

    def insert_many(self, table_name, col_names, values = None):
        placeholder = ",".join(["%s"] * len(col_names))
        if type(col_names) == list or type(col_names) == tuple:
            col_names = ','.join(col_names)
        elif type(col_names) == dict:
            values = list(zip(*(col_names.values())))
            col_names = ','.join(list(col_names.keys()))

        sql = "insert into %s(%s) values (%s)" % (table_name, col_names, placeholder)
        self.__cursor__.executemany(sql, values)
        self.__conn__.commit()

    def __del__(self):
        # close database
        if self.__cursor__:
            self.__cursor__.close()
        if self.__conn__:
            self.__conn__.close()
            print("Disconnected! ")

