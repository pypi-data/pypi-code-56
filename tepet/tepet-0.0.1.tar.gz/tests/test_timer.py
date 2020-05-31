import unittest
from unittest.mock import call

from freezegun import freeze_time

from tepet import Timer
from tests.utils import PatchMixin


class TimerTest(unittest.TestCase, PatchMixin):
    def setUp(self):
        self.printer_mock = self._patch('tepet.timer._printer')

    def assertCallsPrinterCorrectly(self):
        calls = [
            call('1970 Jan 01 00:00:00 +0000 ==== started'),
            call('1970 Jan 01 00:00:00 +0000 ==== elapsed 0.00000 seconds')]
        self.printer_mock.assert_has_calls(calls)
        self.assertEqual(self.printer_mock.call_count, 2)

    def test_timer_works_as_a_contextmanager(self):
        with freeze_time("1970-01-01"):
            with Timer():
                pass
        self.assertCallsPrinterCorrectly()

    def test_timer_works_as_a_decorator(self):
        @Timer()
        def workload():
            pass

        with freeze_time("1970-01-01"):
            workload()
        self.assertCallsPrinterCorrectly()
