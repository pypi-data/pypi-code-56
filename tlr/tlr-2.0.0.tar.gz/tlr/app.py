
"""
Main app module.

It process line string from telnet data that contains certain character in
string. Parsing process is done through regex. So, in one string, items matched
may contain more than one results. Because one line string associated with one
timestamp, we only insert the first result to the database.
"""
import datetime
import logging
import telnetlib

import pytz

from . import constants, models, parser, settings, utils
from .ops import bulk_insert
from .singleton import SingleInstance

logger = logging.getLogger(__name__)


def process_temperature0(timestamp, line, **kwargs):
    """
    Process line string from telnet data that contains string #03.

    Example telnet data: ::

        'T#03 18.70,18.37,91.06,19.85,12.95\r\n \r\n \x8f\x08\x03'

    Note that line from telnet data must be in ordinary string, not in raw
    string.
    """
    if '#03' not in line:
        return

    data_parser = parser.T0Parser()
    data = data_parser.parse_as_dict(line, delimiter=',')

    logger.info('#03 parsing: %s', data)

    if not data:
        return

    if len(data) > 1:
        payload = data[:1]
    else:
        payload = data

    payload[0].update({'timestamp': timestamp})
    bulk_insert(models.engine, models.Temperature0, payload)

    logger.info('#03 payload: %s', payload)


def process_temperature1(timestamp, line, **kwargs):
    """
    Process line string from telnet data that contains string #01.

    Example telnet data: ::

        'T#01 56.92,\r\nT#03 88.10,90.62,90.42,29.68,14.39\r\n \r\n C \xfc'

    Note that line from telnet data must be in ordinary string, not in raw
    string.
    """
    if '#01' not in line:
        return

    data_parser = parser.T1Parser()
    data = data_parser.parse_as_dict(line, delimiter=',')

    logger.info('#01 parsing: %s', data)

    if not data:
        return

    if len(data) > 1:
        payload = data[:1]
    else:
        payload = data

    payload[0].update({'timestamp': timestamp})
    bulk_insert(models.engine, models.Temperature1, payload)

    logger.info('#01 payload: %s', payload)


def process_temperature2(timestamp, line, **kwargs):
    """
    Process line string from telnet data that contains string #02.

    Note that line from telnet data must be in ordinary string, not in raw
    string.
    """
    if '#02' not in line:
        return

    data_parser = parser.T2Parser()
    data = data_parser.parse_as_dict(line, delimiter=',')

    logger.info('#02 parsing: %s', data)

    if not data:
        return

    if len(data) > 1:
        payload = data[:1]
    else:
        payload = data

    payload[0].update({'timestamp': timestamp})
    bulk_insert(models.engine, models.Temperature2, payload)

    logger.info('#02 payload: %s', payload)


def process_emission(timestamp, line, **kwargs):
    """
    Process line string from telnet data that contains string LR0101256.

    Example telnet data: ::

        'TLR0101256 +615.00 +689.00 +646.50 +30.00 +30.30 +30.15 +82.19 +83.04 +82.64 +12.05 \r\n \x80\x0c'

    Note that line from telnet data must be in ordinary string, not in raw
    string.
    """
    if 'LR0101256' not in line:
        return

    data_parser = parser.EParser()
    data = data_parser.parse_as_dict(line, delimiter=' ')

    logger.info('LR0101256 parsing: %s', data)

    if not data:
        return

    if len(data) > 1:
        payload = data[:1]
    else:
        payload = data

    payload[0].update({'timestamp': timestamp})
    bulk_insert(models.engine, models.Emission, payload)

    logger.info('LR0101256 payload: %s', payload)


class App(SingleInstance):
    """
    TLR main app class.

    We run the app in the single instance mode so that only one process listen
    to the telnet server and process the data.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        """
        Listen to telnet server for incoming data and process it immediately.
        """
        with telnetlib.Telnet(host=settings.TELNET_HOST,
                              port=settings.TELNET_PORT,
                              timeout=settings.TELNET_CONNECT_TIMEOUT) as tn:
            logger.info('Listening to telnet server at %s:%s',
                        settings.TELNET_HOST, settings.TELNET_PORT)

            data = utils.decode_string(
                tn.read_until(b'\n\n', settings.TELNET_TIMEOUT))
            line = utils.force_str(data, errors='backslashreplace')

            if len(line) >= constants.MIN_LINE_LENGTH_TO_PROCESS:
                logger.info('raw: %s', str(data))

                now = datetime.datetime.now(pytz.timezone(settings.TIMEZONE))
                process_temperature0(now, line)
                process_temperature1(now, line)
                process_temperature2(now, line)
                process_emission(now, line)
