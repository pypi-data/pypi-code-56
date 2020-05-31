import os
import sys
import sqlite3
from calendar import timegm
from datetime import datetime, timedelta, date
from time import gmtime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

__VERSION__ = "1.0"
__AUTHOR__ = "Carlos Tangerino"

TS = 0
VALUE = 1
STATUS = 2
MAX_EPOCH_SEC = 9999999999


class Job:
    JOB_TYPE_HOUR = 0
    JOB_TYPE_DAY = 1
    JOB_TYPE_MONTH = 2
    JOB_TYPE_YEAR = 3


class Timeseries:
    STATUS_OK = 0
    STATUS_ESTIMATED = 1
    STATUS_LAST = 2
    STATUS_NULL = 3
    STATUS_CONSTANT = 4
    STATUS_OVERFLOW = -1
    STATUS_UNDERFLOW = -2
    STATUS_GAP = -3
    STATUS_INCREMENT = -4
    STATUS_DECREMENT = -5
    STATUS_UNKNOWN = -6

    def __init__(self, name=None):
        self.data_points = []
        self.name = name

    def add(self, time_stamp, value, status=STATUS_OK):
        epoch = date_to_epoch(time_stamp)
        if epoch is None:
            raise Exception("Invalid time stamp type")
        dp = [epoch, value, status]
        self.data_points.append(dp)

    def sort(self):
        self.data_points.sort(key=lambda x: x[TS])

    def __repr__(self):
        body = ""
        for dp in self.data_points:
            if dp[TS] > MAX_EPOCH_SEC:
                tm = gmtime(dp[TS] / 1000)
                msec = dp[TS] % 1000
            else:
                tm = gmtime(dp[TS])
                msec = None
            dt = datetime(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec)
            if msec is None:
                entry = "[{}, {}, {}]".format(dt, dp[VALUE], dp[STATUS])
            else:
                entry = "[{}.{:03}, {}, {}]".format(dt, msec, dp[VALUE], dp[STATUS])
            body += entry
        return "Timeseries(%s,%s)" % (self.name, body)

    def __len__(self):
        return len(self.data_points)

    def to_dict(self):
        o = []
        for dp in self.data_points:
            dt = epoch_to_date(dp[TS]).strftime("%Y-%m-%dT%H:%M:%S")
            item = [dt, _int_if_possible(dp[VALUE]), dp[STATUS]]
            o.append(item)
        return o


def epoch_to_date(utc):
    if utc > MAX_EPOCH_SEC:
        us = (utc % 1000) * 1000
        epoch = int(utc / 1000)
    else:
        us = 0
        epoch = utc
    tm = gmtime(epoch)
    return datetime(
        tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec, microsecond=us
    )


def date_to_epoch(date_value):
    if isinstance(date_value, str):
        # mas pode ser um numero
        try:
            time_stamp = int(date_value)
            return time_stamp
        except:
            pass
        dt = parse(date_value)
        tt = dt.timetuple()
        time_stamp = timegm(tt)
    elif isinstance(date_value, (datetime, date)):
        tt = date_value.timetuple()
        time_stamp = timegm(tt)
    elif isinstance(date_value, int):
        time_stamp = date_value
    elif isinstance(date_value, float):
        time_stamp = int(date_value)
    else:
        time_stamp = None
    if time_stamp and time_stamp < MAX_EPOCH_SEC:
        time_stamp *= 1000
    return time_stamp


def _int_if_possible(number):
    i = int(number)
    if i == number:
        return i
    return number


def _stringfy_list(id_list):
    if isinstance(id_list, (float, int)):
        id_list = [str(id_list)]
    else:
        for s in range(len(id_list)):
            id_list[s] = str(id_list[s])
    return id_list


def _get_eoi_query(sensor_id, eoi, sd, ed):
    q = '''
        REPLACE INTO rollup (sensor_id,
                             type,
                             ts,
                             vsum,
                             vmax,
                             vmin,
                             vcount,
                             vavg)
        SELECT 
            {} "id",
            0 "type",
            strftime('%s', strftime('%Y-%m-%d %H:00:00', (ts/1000) - {}, 'unixepoch')) "ts",
            IFNULL(SUM(value),0) "sum",
            IFNULL(MAX(value),0) "max",
            IFNULL(MIN(value),0) "min",
            IFNULL(COUNT(value),0) "count",
            CASE
            WHEN COUNT(value) > 0 THEN SUM(value)/COUNT(value)
            ELSE 0
            END "avg"
        FROM series
        WHERE sensor_id = {}
        AND status >= 0
        {}
        GROUP BY 3
    '''
    seconds = '1' if eoi else '0'
    t = '''
            AND ts >= {} 
            AND ts <= {} 
        '''
    time_range = t.format(sd, ed)
    return q.format(sensor_id, seconds, sensor_id, time_range)


def _rollup_job_hour(conn, sensor_id, jobs):
    sd = int(sys.float_info.max - 1)
    ed = -sd
    for k, _ in jobs.items():
        if k < sd:
            sd = k
        if k > ed:
            ed = k
    ed += 3600
    query = _get_eoi_query(sensor_id, False, sd * 1000, ed * 1000)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        s = "ERROR: rollup_job_hour - {} -{}".format(e, query)
        raise Exception(s)


def _get_dmy_query(sensor_id, job_type, source_type, sd, ed):
    if job_type == Job.JOB_TYPE_DAY:
        dt_fmt = "%Y-%m-%d 00:00:00"
    elif job_type == Job.JOB_TYPE_MONTH:
        dt_fmt = "%Y-%m-01 00:00:00"
    else:
        dt_fmt = "%Y-01-01 00:00:00"
    q = '''
        REPLACE INTO rollup (sensor_id, type, ts, vsum, vmax, vmin, vcount, vavg)
        SELECT 
            {}, {},
            strftime('%s',strftime('{}', ts, 'unixepoch')),
            SUM(vsum), 
            MAX(vmax), 
            MIN(vmin), 
            SUM(vcount),
            CASE
            WHEN SUM(vcount) > 0 THEN SUM(vsum)/SUM(vcount)
            ELSE 0
            END
            FROM
                rollup
            WHERE
                sensor_id = {} AND type = {}
                    AND ts >= {}
                    AND ts < {}
            GROUP BY 3
    '''
    return q.format(sensor_id, job_type, dt_fmt, sensor_id, source_type, sd, ed)


def _rollup_job_dmy(conn, sensor_id, jobs, job_type, source_type):
    sd = sys.float_info.max
    ed = sys.float_info.min
    for k, _ in jobs.items():
        if k < sd:
            sd = k
        if k > ed:
            ed = k
    dt = epoch_to_date(sd)
    if job_type == Job.JOB_TYPE_DAY:
        dt += timedelta(days=1)
    elif job_type == Job.JOB_TYPE_MONTH:
        dt += relativedelta(months=1)
    else:
        dt += relativedelta(months=12)
    ed = date_to_epoch(dt)
    query = _get_dmy_query(sensor_id, job_type, source_type, sd, ed)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        s = "ERROR: rollup_job_dmy - {} - {}".format(e, query)
        raise Exception(s)


def _rollup_job(db, job_type, sensor_id, jobs):
    try:
        if job_type == Job.JOB_TYPE_HOUR:
            _rollup_job_hour(db, sensor_id, jobs)
        elif job_type == Job.JOB_TYPE_DAY:
            _rollup_job_dmy(db, sensor_id, jobs, Job.JOB_TYPE_DAY, Job.JOB_TYPE_HOUR)
        elif job_type == Job.JOB_TYPE_MONTH:
            _rollup_job_dmy(db, sensor_id, jobs, Job.JOB_TYPE_MONTH, Job.JOB_TYPE_DAY)
        elif job_type == Job.JOB_TYPE_YEAR:
            _rollup_job_dmy(db, sensor_id, jobs, Job.JOB_TYPE_YEAR, Job.JOB_TYPE_MONTH)
        else:
            raise Exception("rollup_job - Invalid job type - {}".format(job_type))
    except Exception as e:
        s = "ERROR - rollup_job - Type: {} - {}".format(job_type, e)
        raise Exception(s)


def _reduce_jobs(jobs, job_type):
    new_jobs = {}
    for ts, _ in jobs.items():
        dt = epoch_to_date(ts)
        if job_type == Job.JOB_TYPE_HOUR:
            dt = datetime(dt.year, dt.month, dt.day)
        elif job_type == Job.JOB_TYPE_DAY:
            dt = datetime(dt.year, dt.month, 1)
        elif job_type == Job.JOB_TYPE_MONTH:
            dt = datetime(dt.year, 1, 1)
        epoch = date_to_epoch(dt) // 1000
        new_jobs[epoch] = 1
    return new_jobs


def _rollup_sensor(conn, sensor_id, jobs):
    job_type = [Job.JOB_TYPE_HOUR, Job.JOB_TYPE_DAY, Job.JOB_TYPE_MONTH, Job.JOB_TYPE_YEAR]
    for jt in job_type:
        _rollup_job(conn, jt, sensor_id, jobs)
        jobs = _reduce_jobs(jobs, jt)


def _fetchall(query, conn):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def _rebuild(conn):
    create_stm = [
        "DROP TABLE IF EXISTS rollup",
        "DROP TABLE IF EXISTS series",
        "DROP TABLE IF EXISTS sensors",
        "PRAGMA foreign_keys=OFF;",
        '''CREATE TABLE sensors (
          id           integer PRIMARY KEY AUTOINCREMENT,
          name         text NOT NULL,
          ttl          integer DEFAULT 0,
          tags         json NOT NULL DEFAULT '{}',
          /* Keys */
          CONSTRAINT sensors_idx_name
            UNIQUE (name)
        );''',
        '''CREATE TABLE series (
          id         integer PRIMARY KEY AUTOINCREMENT,
          sensor_id  integer NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
          ts         integer NOT NULL,
          value      real NOT NULL,
          status     integer NOT NULL DEFAULT 0,
          /* Keys */
          UNIQUE (sensor_id, ts) ON CONFLICT REPLACE
        );''',
        '''CREATE TABLE rollup (
          id         integer PRIMARY KEY AUTOINCREMENT,
          sensor_id  integer NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
          ts         integer,
          type       integer,
          vmin       real,
          vmax       real,
          vavg       real,
          vsum       real,
          vcount     integer,
          /* Keys */
          CONSTRAINT rollup_unique_idx
            UNIQUE (sensor_id, type, ts)
        );''',
        '''CREATE INDEX idx_data_store_id_sec
          ON series
          (sensor_id, ts);''',
        '''CREATE INDEX idx_data_store_sec
          ON series
          (ts);'''
    ]
    for cmd in create_stm:
        conn.execute(cmd)


def _get_sensor_id(conn, sensor_name):
    cur = conn.cursor()
    q = "SELECT id FROM sensors WHERE name='{}'".format(sensor_name)
    cur.execute(q)
    rows = cur.fetchone()
    if rows is None:
        return rows
    return rows[0]


def _get_ts_hour(time_stamp):
    epoch = time_stamp // 1000
    tm = gmtime(epoch)
    dt = datetime(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, 0, 0)
    tt = dt.timetuple()
    time_stamp = timegm(tt)
    return time_stamp


class Datastore:
    hour = "hour"
    day = "day"
    month = "month"
    year = "year"
    vmax = "max"
    vmin = "min"
    vcount = "count"
    vavg = "avg"
    vsum = "sum"

    def __init__(self, database, user_name=None, password=None, create=False):
        new_file = False
        if not os.path.exists(database):
            new_file = True
            if not create:
                raise Exception("Database not found")
        self.database = database
        self.user_name = user_name
        self.password = password
        self.conn = None
        self.must_rebuild = new_file or create
        self.is_opened = False

    def open(self):
        try:
            self.conn = sqlite3.connect(self.database)
        except Exception as e:
            s = "sqlite3.connect({}) -> {}".format(self.database, e)
            print(s)
            raise Exception(s)

        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA busy_timeout = 30000;")
        if self.must_rebuild:
            _rebuild(self.conn)
        self.is_opened = True

    def close(self):
        if self.is_opened:
            self.conn.close()
            self.is_opened = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def rebuild(self):
        _rebuild(self.conn)

    def create(self, time_series, ttl=0):
        try:
            jobs = {}
            id = _get_sensor_id(self.conn, time_series.name)
            cur = self.conn.cursor()
            if id is None:
                q = "INSERT INTO sensors (name, ttl) VALUES ('{}', {})".format(time_series.name, ttl)
                cur.execute(q)
                self.conn.commit()
                id = cur.lastrowid
            q = "INSERT INTO series (sensor_id, ts, value, status) VALUES "
            dp_count = 0
            for dp in time_series.data_points:
                if dp_count > 0:
                    q += ",\n"
                row = "({}, {}, {}, {})".format(id, dp[TS], dp[VALUE], dp[STATUS])
                q += row
                dp_count += 1
                hour = _get_ts_hour(dp[TS])
                # print("NEW JOB {} {} {} {}".format(hour, dp[TS], epoch_to_date(hour), epoch_to_date(dp[TS])))
                jobs[hour] = hour
            cur.execute(q)
            self.conn.commit()
            _rollup_sensor(self.conn, id, jobs)
        except Exception as e:
            print("ERROR - data_create - {} - {}".format(e, time_series))

    def sensors(self):
        query = '''
            SELECT id, name, ttl FROM sensors ORDER BY id
        '''
        sensors = []
        rows = _fetchall(query, self.conn)
        for row in rows:
            sensors.append({"id": row[0], "name": row[1], "ttl": row[2]})
        return sensors

    def ttl(self, sensor_id, ttl):
        q = ""
        try:
            cur = self.conn.cursor()
            if id is None:
                q = "UPDATE sensors SET ttl={} where id = {}".format(sensor_id, ttl)
                cur.execute(q)
                self.conn.commit()
                return True
        except Exception as e:
            print("datastore:ttl - {} - {}".format(q, e))
            return False

    def raw(self, id_list, start_date, end_date, iso_date=False):
        """
        Read series from the interval table
        :param iso_date:
        :param id_list: List with sensor's id
        :param start_date: The start date
        :param end_date: The end date
        :return: Time series
        """
        id_list = _stringfy_list(id_list)
        sd = date_to_epoch(start_date)
        ed = date_to_epoch(end_date)
        if sd is None or ed is None:
            raise Exception("Invalid date")
        q = '''
            SELECT h.ts, h.value, h.status, s.id FROM series h
            JOIN sensors s ON (h.sensor_id = s.id)
            AND s.id IN ({})
            AND ts >= {} 
            AND ts <= {}
        '''
        key_list = ",".join(id_list)
        query = q.format(key_list, sd, ed)
        rows = _fetchall(query, self.conn)
        telemetry_list = {}
        for row in rows:
            sensor_id = row[3]
            if sensor_id in telemetry_list:
                item = telemetry_list[sensor_id]
            else:
                item = []
                telemetry_list[sensor_id] = item
            dt = epoch_to_date(row[0]).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] if iso_date else row[0]
            item.append({"ts": dt, "value": row[1]})
        return telemetry_list

    def rollup(self, id_list, start_date, end_date, group_by, function, iso_date=False):
        id_list = _stringfy_list(id_list)
        sd = date_to_epoch(start_date) // 1000
        ed = date_to_epoch(end_date) // 1000
        if sd is None or ed is None:
            raise Exception("Invalid date")
        groups = [
            "hour", "day", "month", "year"
        ]
        if group_by not in groups:
            raise Exception("Invalid group")
        functions = [
            "max", "min", "count", "sum", "avg", "first", "last"
        ]
        if function not in functions:
            raise Exception("Invalid function")
        if group_by == "day":
            rollup_type = Job.JOB_TYPE_DAY
        elif group_by == "hour":
            rollup_type = Job.JOB_TYPE_HOUR
        elif group_by == "month":
            rollup_type = Job.JOB_TYPE_MONTH
        else:
            rollup_type = Job.JOB_TYPE_YEAR
        if function in ["first", "last"]:
            raise Exception("Function not implemented")
        q = '''
            SELECT h.ts, h.v{}, 0, s.id FROM rollup h
            JOIN sensors s ON (h.sensor_id = s.id)
            AND s.id IN ({})
            AND type = {}
            AND ts >= {} 
            AND ts <= {}
        '''
        key_list = ",".join(id_list)
        query = q.format(function, key_list, rollup_type, sd, ed)
        rows = _fetchall(query, self.conn)

        telemetry_list = {}
        for row in rows:
            sensor_id = row[3]
            if sensor_id in telemetry_list:
                item = telemetry_list[sensor_id]
            else:
                item = []
                telemetry_list[sensor_id] = item
            dt = epoch_to_date(row[0]).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] if iso_date else row[0]
            item.append({"ts": dt, "value": row[1]})
        return telemetry_list

    def raw_dump(self, start_index, limit=100):
        q = '''
            SELECT id, sensor_id, ts, value, status
            FROM series
            WHERE id >= {}
            LIMIT {}
        '''
        query = q.format(start_index, limit)
        rows = _fetchall(query, self.conn)
        d = []
        for row in rows:
            dt = epoch_to_date(row[2]).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            item = {
                "id": row[0],
                "sensor_id": row[1],
                "ts": dt,
                "value": _int_if_possible(row[3]),
                "status": row[4]
            }
            d.append(item)
        return d

    def rollup_dump(self, start_index, limit=100):
        q = '''
            SELECT id, sensor_id, type, ts, vmax, vmin, vsum, vcount, vavg
            FROM rollup
            WHERE id >= {}
            LIMIT {}
        '''
        query = q.format(start_index, limit)
        rows = _fetchall(query, self.conn)
        d = []
        for row in rows:
            dt = epoch_to_date(row[3]).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            item = {
                "id": row[0],
                "sensor_id": row[1],
                "type": row[2],
                "ts": dt,
                "max": _int_if_possible(row[4]),
                "min": _int_if_possible(row[5]),
                "sum": _int_if_possible(row[6]),
                "count": _int_if_possible(row[7]),
                "avg": _int_if_possible(row[8])
            }
            d.append(item)
        return d

    def delete(self, sensor_id, start_date, end_date):
        sd = date_to_epoch(start_date)
        ed = date_to_epoch(end_date)
        if sd is None or ed is None:
            raise Exception("Invalid date")
        q = ""
        try:
            cur = self.conn.cursor()
            if id is None:
                q = "DELETE series WHERE sensor_id = {} and ts >= {} and ts <= {}".format(sensor_id, start_date, end_date)
                cur.execute(q)
                self.conn.commit()
                return True
        except Exception as e:
            print("datastore:delete - {} - {}".format(q, e))
            return False

    def purge(self):
        q = ""
        try:
            cur = self.conn.cursor()
            if id is None:
                q = """
                DELETE series h
                JOIN sensors s ON (sensors.id = h.series_id)
                WHERE 
                h.ts < ((1000 * strftime('%s','now')) - (s.ttl * 1000)) 
                """
                cur.execute(q)
                self.conn.commit()
                return True
        except Exception as e:
            print("datastore:purge - {} - {}".format(q, e))
            return False
