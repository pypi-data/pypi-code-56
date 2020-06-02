import unittest
from unittest import mock

import time

from sett.cli.progress import format_eta, CliProgress

param_list = [(1, '1'), (10, '10'), (100, '01:40'),
              (1000, '16:40'), (10000, '02:46:40')]


class TestCliProgress(unittest.TestCase):

    def test_format_eta(self):
        for eta_secs, expected in param_list:
            with self.subTest(msg="format_eta", eta_secs=eta_secs, expected=expected):
                self.assertEqual(format_eta(eta_secs), expected)

    @mock.patch('sett.cli.progress.sys.stdout')
    def test_cli_progress(self, mock_stdout):
        class StartsWith(str):
            def __eq__(self, other: str):
                return other.startswith(self)

        bar_length = 10
        cli_progress = CliProgress(
            fill="*", initial_print=False, bar_length=bar_length)
        cli_progress.print_current()
        mock_stdout.write.assert_called_once_with(
            f"\r|{'-' * bar_length}| 0.0%")
        # Reset the mock before continuing
        mock_stdout.reset_mock()
        # Sleep for 1.1s before the next invocation so that 'print_current'
        # gets automatically invoked
        time.sleep(1.1)
        cli_progress.update(.34)
        mock_stdout.write.assert_called_once_with(
            StartsWith("\r|***-------| 34.0%"))
