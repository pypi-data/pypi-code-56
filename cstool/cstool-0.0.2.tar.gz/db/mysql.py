import pymysql


class DBUtil:

    def __init__(self, config):
        self.config = config
        self._conn = None
        self._debug = True
        if not config.get('debug'):
            self._debug = False
        pass

    def get_conn(self):
        if not self._conn:
            self._conn = pymysql.connect(host=self.config['dbHost'], user=self.config['dbUser'], passwd=self.config['dbPwd'], db=self.config['dbName'])
        return self._conn

    def connect(self):
        self._conn = self.get_conn()
        return self

    def disconnect(self):
        conn = self._conn
        if conn:
            conn.close()

    def update(self, sql):
        conn = self._conn
        cur = conn.cursor()
        if self._debug:
            print(sql)
        ret = cur.execute(sql)
        conn.commit()
        cur.close()
        return ret

    def query(self, sql):
        conn = self._conn
        cur = conn.cursor()
        if self._debug:
            print(sql)
        cur.execute(sql)
        col = cur.description
        rows = cur.fetchall()
        cur.close()
        ret = []
        # 加上字段名，返回map对象
        for row in rows:
            obj = {}
            for i in range(len(row)):
                obj[col[i][0]] = row[i]
            ret.append(obj)

        return ret


def new(config):
    return DBUtil(config)
