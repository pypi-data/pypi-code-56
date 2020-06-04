"""InOutScan"""
import json
import sqlite3
import sys
import time

import requests
import serial

from . import __version__


class InOutScan():
    """
    InOutScan - Publish incoming serial strings to an API
    """

    def __init__(self):
        self.database = 'inout_scan.db'
        self.init_local_database()
        self.serial_details = None
        self.api_details = None
        self.serial_connection = None
        self.scanner = None

    def set_api(self, api_details):
        """
        Set API configuration
        """
        self.api_details = api_details

    def set_serial(self, serial_details):
        """
        Set serial configuration
        """
        self.serial_details = serial_details

    def set_scanner(self, scanner):
        """
        Set scanner name
        """
        self.scanner = scanner

    def init_serial(self):
        """initialize serial port"""
        try:
            print(self.serial_details['port'], self.serial_details['baudrate'])
            print("Connecting to the serial port... ")
            # connect to serial port
            self.serial_connection = serial.Serial(
                self.serial_details['port'],
                self.serial_details['baudrate'],
                timeout=None
            )
        except serial.SerialException as err:
            print("Error: Failed to connect serial: " + err.strerror)
            # unable to continue with no serial input
            raise SystemExit

        self.serial_connection.flushInput()

    def init_local_database(self):
        """
        creates a local sqlite database
        """
        try:
            self.sqlite_connection = sqlite3.connect(self.database)
            sqlite_create_table_query = '''CREATE TABLE inout_events (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                badge TEXT NOT NULL,
                                timestamp INTEGER,
                                scanner TEXT NOT NULL,
                                sentToApi BOOLEAN
                                );'''
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sqlite_create_table_query)
            print("Successfully created the "
                  "sqlite database {}".format(self.database))
        except sqlite3.Error:
            pass

    def scan(self):
        """Loop that handles incoming serial strings"""
        self.init_serial()
        try:
            line = ''
            while True:
                for character in self.serial_connection.read():
                    # stop collecting characters when a newline is received
                    if character == 13:
                        data = {
                            'badge': line.strip(),
                            'timestamp': int(time.time()),
                            'scanner': self.scanner,
                        }
                        sent_to_api = self.publish(data)
                        data.update({'sentToApi': sent_to_api})
                        self.write_to_localdb(data)

                        # start with an empty string
                        line = ''
                    else:
                        line += chr(character)

        # handle app closure
        except KeyboardInterrupt:
            print("Interrupt received")
            self.cleanup()
        except serial.serialutil.SerialException:
            print("Something went wrong with the serial communication")
            self.cleanup()
        except RuntimeError:
            print("uh-oh! time to die")
            self.cleanup()

    def flush(self):
        """submit all pending data to the API"""
        self.sqlite_connection.row_factory = sqlite3.Row
        cur = self.sqlite_connection.cursor()
        # get pending data
        cur.execute('''
            SELECT id, badge, timestamp, scanner FROM inout_events
            WHERE sentToApi = 0
            ''')

        while True:
            data = cur.fetchone()
            if data is None:
                break
            data = dict(data)
            if self.publish(data):
                self.write_to_localdb(data)

        # remove published records
        self.clear()

    def publish(self, data):
        """Publish string to API"""
        success = False
        try:
            response = requests.post(
                url=self.api_details['api_url'],
                headers={
                    'Authorization': 'Basic {}'.format(
                        self.api_details['api_key']),
                    'User-Agent': 'inout_scan/{version}'.format(
                        version=__version__),
                    'Content-type': 'application/json'},
                data=json.dumps(data),
                timeout=1
                )
            print("HTTP status code: ", response.status_code)
            response.raise_for_status()
            success = True
        except requests.exceptions.ConnectionError:
            # failed to submit data
            print("Could not connect to API")
            success = False
        except requests.exceptions.HTTPError:
            # failed to submit data
            print("An HTTP error occurred")
            success = False
        except Exception:
            print("Something went wrong")
            success = False

        return success

    def write_to_localdb(self, data):
        """
        write events to a local sqlite database
        """
        print("write to localdb: ", data)
        if "id" in data:
            query = """UPDATE inout_events
                       SET
                          sentToApi = 1
                       WHERE
                          id = :id
                    """
        else:
            print("insert")
            query = """INSERT INTO inout_events
                          (badge,  timestamp,  scanner,  sentToApi)
                       VALUES
                          (:badge, :timestamp, :scanner, :sentToApi)
                    """

        cursor = self.sqlite_connection.cursor()
        cursor.execute(query, data)
        self.sqlite_connection.commit()

    def clear(self):
        """
        Remove all data from the cache file that has
        successfully been submitted
        """
        query = """DELETE FROM inout_events
                   WHERE sentToApi = 1
                """
        cursor = self.sqlite_connection.cursor()
        cursor.execute(query)
        self.sqlite_connection.commit()

    def cleanup(self):
        """
        close serial connection
        """
        print("Ending and cleaning up")
        self.serial_connection.close()
        self.sqlite_connection.close()
        print("The SQLite connection is closed")


def main():
    """
    main
    """
    sys.exit(0)


if __name__ == "__main__":
    main()
