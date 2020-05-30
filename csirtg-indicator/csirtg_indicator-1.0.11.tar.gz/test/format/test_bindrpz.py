import pytest
from csirtg_indicator.format.zbindrpz import BindRPZ, get_lines
from csirtg_indicator import Indicator
from pprint import pprint
import re

@pytest.fixture
def indicator():
    i = {
        'indicator': "example.com",
        'provider': "me.com",
        'tlp': "amber",
        'confidence': "85",
        'reporttime': '2015-01-01T00:00:00Z',
        'itype': 'fqdn'
    }
    return Indicator(**i)


def test_format_bindrpz(indicator):
    data = [indicator]
    text = str(BindRPZ(data))

    assert re.findall(r'^;;; generated by: csirtg-indicator at \S+', text)
    assert re.findall(r'@\s+IN\s+NS\s+localhost.', text)
    assert re.findall(r'example.com\s+CNAME .', text)
    assert re.findall(r'\*\.example.com\s+CNAME .', text)


def test_format_bindrpz2(indicator):

    data = [indicator, indicator]
    n = list(get_lines(data))
    assert len(n) > 0

if __name__ == '__main__':
    test_format_bindrpz()
