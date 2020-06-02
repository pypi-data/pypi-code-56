import re
import abc
import logging

from .utils import force_str, get_value_or_none


logger = logging.getLogger(__name__)


class ParserError(Exception):
    pass


class BaseParser(object):
    """
    Base parser object to parse telnet data.
    """

    fields = []

    @abc.abstractmethod
    def parse(self, s, **kwargs):
        pass

    def parse_as_list(self, s,
                      delimiter=',',
                      converter=float,
                      **kwargs):
        """
        Parse string s as list. Empty value will be discarded. If converter is
        not None, each value in the list will be converted using the converter
        function.

        Note that this method always return a list of list of all items matched
        in the regex.
        """
        cleaned_data = []
        data = self.parse(s, **kwargs)
        for item in data:
            d = []
            for field in item.split(delimiter):
                if not field:
                    continue

                if converter is not None:
                    try:
                        value = converter(field)
                    except ValueError as e:
                        logger.error(e)
                        value = None
                else:
                    value = force_str(field)

                d.append(value)
            cleaned_data.append(d)
        return cleaned_data

    def parse_as_dict(self, s, **kwargs):
        """
        Parse string s as dictionary. Return truncated version if fields length
        less than or greater than list parsed.

        Note that this method always return a list of dictionary of all items
        matched in the regex.
        """
        if not self.fields:
            raise ParserError(
                'Parsing as dictionary requires fields to be set')

        cleaned_data = []
        data = self.parse_as_list(s, **kwargs)
        for item in data:
            d = dict([
                (k, get_value_or_none(item, i))
                for i, k in enumerate(self.fields)
            ])
            cleaned_data.append(d)
        return cleaned_data


class TParser(BaseParser):
    """
    Base temperature parser object.
    """

    regex = re.compile(r'')

    def parse(self, s, **kwargs):
        return self.regex.findall(s)


class T0Parser(TParser):

    regex = re.compile(r'.*#03\s(?P<data>[0-9].*[.,].*)\r')
    fields = [
        'temperature1',
        'temperature2',
        'temperature3',
        'temperature4',
        'battery_voltage',
    ]


class T1Parser(TParser):
    """
    Parser object for parsing telnet on tlr.models.Temperature1 model.

    Note that there are no timestamp on telnet data. So we only parse
    temperature value.
    """

    regex = re.compile(r'.*#01\s(?P<data>[0-9].*[.,].*)\r')
    fields = ['temperature', ]


class T2Parser(TParser):
    """
    Parser object for parsing telnet on tlr.models.Temperature2 model.

    Note that there are no timestamp on telnet data. So we only parse
    temperature value.
    """

    regex = re.compile(r'.*#02\s(?P<data>[0-9].*[.,].*)\r')
    fields = ['temperature', ]


class EParser(BaseParser):
    """
    Parser object for parsing telnet on tlr.models.Emission model.

    Note that there are no timestamp on telnet data.
    """

    regex = re.compile(r'.*TLR0101256\s(?P<data>\+[0-9].*[.,].*)\r')
    fields = [
        'co2_min',
        'co2_max',
        'co2_avg',
        'temperature_min',
        'temperature_max',
        'temperature_avg',
        'humidity_min',
        'humidity_max',
        'humidity_avg',
        'input_battery_voltage',
    ]

    def parse(self, s, **kwargs):
        return self.regex.findall(s)
