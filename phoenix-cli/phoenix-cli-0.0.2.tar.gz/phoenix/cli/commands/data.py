import datetime
import sys

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

from knack.log import get_logger

logger = get_logger(__name__)

BUFFER_SIZE = 16 * 1024


def ingest(csv_file, keyspace, cassandra_hosts=["127.0.0.1"], read_buffer_size=None):
    """ Ingest data frm csv file

    :param csv_file: CSV file to import
    :type csv_file: str

    :param keyspace: Cassandra keyspace
    :type keyspace: str

    :param cassandra_hosts: Cassandra hosts comma-delimited list of addresses. Ex: "<ip1>,<ip2>,<ip3>"
    :type cassandra_hosts: str

    :param read_buffer_size: Buffer size in bytes when read csv. Too large buffer size can make Cassandra error "Batch too large"
    :type read_buffer_size: int
    """

    if isinstance(cassandra_hosts, str):
        cassandra_hosts = cassandra_hosts.split(",")

    if read_buffer_size is None:
        read_buffer_size = BUFFER_SIZE

    cluster = Cluster(cassandra_hosts)
    session = cluster.connect(keyspace)

    with open(csv_file, "r", encoding="utf-8-sig") as f:
        line_count = 0
        record_count = 0
        t0 = datetime.datetime.now()
        lines = f.readlines(read_buffer_size)
        futures = []

        while lines:
            sensors = [Sensor(line) for line in lines]
            future = batch_insert(session, sensors)

            futures.append(future)

            line_count += len(lines)
            elapse_time = max(
                datetime.timedelta(seconds=1), datetime.datetime.now() - t0
            )
            logger.warn(
                f"\x1b[1Aingest {line_count} rows ({line_count/elapse_time.seconds:12.4f} rps) {' ': <50}"
            )
            lines = f.readlines(read_buffer_size)

        for future in futures:
            rows = future.result()
            record_count += len(rows.response_future.query._statements_and_parameters)

        logger.warn(f"\nline_count={line_count}")
        logger.warn(f"record_count={record_count}")

    return {
        "csv_file": csv_file,
        "cassandra_hosts": cassandra_hosts,
        "total_lines": line_count,
        "total_records": record_count,
    }


class Sensor:
    PREFIX = "UT_IOT_"

    def __init__(self, line):
        row = self._parse(line)
        self.raw = line
        self.tag = row[1]
        self.timestamp = self._get_timestamp(row[0])
        self.date = self.timestamp.date()
        self.machine, self.sensor = row[1].split(".")
        self.operation = self.machine.split("_")[0]
        self.value = row[2] if row[2].lower() != "null" else None

    def __repr__(self):
        return self.raw

    def _parse(self, line):
        return line.replace(self.PREFIX, "").rstrip("\n").split(",")

    def to_meta(self):
        return (
            (f"operation={self.operation}", f"{self.tag}"),
            (f"machine={self.machine}", f"{self.tag}"),
            (f"sensor={self.sensor}", f"{self.tag}"),
            (f"tag={self.tag}", f"{self.date}"),
        )

    def to_operation(self):
        return (self.operation, self.machine)

    def to_machine(self):
        return (self.machine, self.sensor)

    def to_sensor(self):
        return (self.tag, self.date, self.timestamp, self.value)

    def _get_timestamp(self, timestamp: str):
        d, t = timestamp.split(" ")
        dd = d.split("-")
        tt = t.split(":")
        s, us = tt[2].split(".")
        return datetime.datetime(
            int(dd[0]),
            int(dd[1]),
            int(dd[2]),
            int(tt[0]),
            int(tt[1]),
            int(s),
            int(us[:6]),
        )


def handle_success(rows):
    # print(rows)
    pass


def handle_error(exception, batch):
    logger.error("Failed to fetch user info: %s", exception)
    logger.error(batch)


def batch_insert(session, data):
    batch = BatchStatement()

    meta_data = {meta for datum in data for meta in datum.to_meta()}
    operation_data = {datum.to_operation() for datum in data}
    machine_data = {datum.to_machine() for datum in data}
    sensor_data = [datum.to_sensor() for datum in data]

    meta_statement = session.prepare("INSERT INTO metadata(name, value) VALUES (?, ?)")
    for row in meta_data:
        batch.add(meta_statement, row)

    operation_statement = session.prepare(
        "INSERT INTO operation(name, machine_name) VALUES (?, ?)"
    )
    for row in operation_data:
        batch.add(operation_statement, row)

    machine_statement = session.prepare(
        "INSERT INTO machine(name, sensor_name) VALUES (?, ?)"
    )
    for row in machine_data:
        batch.add(machine_statement, row)

    sensor_statement = session.prepare(
        "INSERT INTO sensor(tag_name, date, timestamp, value) VALUES (?, ?, ?, ?)"
    )
    for row in sensor_data:
        batch.add(sensor_statement, row)

    future = session.execute_async(batch)
    future.add_callbacks(handle_success, handle_error, errback_args=(batch,))

    return future
