from unittest import TestCase

from jsm_user_services.support.http_utils import request
from requests.exceptions import ConnectTimeout


class TestContracts(TestCase):
    def test_should_raise_timeout(self):

        with request() as r:
            # check https://stackoverflow.com/a/100859 for the reason of "http://www.google.com:81/"
            self.assertRaises(ConnectTimeout, r.get, "http://www.google.com:81/")
