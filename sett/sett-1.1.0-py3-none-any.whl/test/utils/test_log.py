import unittest
from unittest import mock
import logging

from sett.utils import log


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.messages = {}
        super().__init__(*args, **kwargs)

    def emit(self, record):
        self.messages.setdefault(
            record.levelname.lower(), []).append(record.getMessage())


class TestLog(unittest.TestCase):
    def test_exception_to_message(self):
        logger = logging.getLogger()
        mock_handler = MockLoggingHandler()
        logger.addHandler(mock_handler)

        @log.exception_to_message(ValueError)
        def f():
            raise ValueError("TestError")

        mock_exit = mock.Mock()
        with mock.patch('sys.exit', mock_exit):
            f()
        mock_exit.assert_called_once_with(1)
        self.assertEqual(mock_handler.messages, {'error': ["TestError"]})

        mock_handler.messages = {}
        m = mock.Mock()
        f(on_error=m)  # pylint: disable=unexpected-keyword-arg
        self.assertEqual(mock_handler.messages, {'error': ["TestError"]})
        m.assert_called_once_with()

    @staticmethod
    def test_log_task_success():
        mock_log_ok = mock.Mock()
        mock_log_err = mock.Mock()
        with log.LogTask("Testing", ok_logger=mock_log_ok,
                         err_logger=mock_log_err):
            pass
        mock_log_err.assert_not_called()
        mock_log_ok.assert_has_calls([mock.call("Testing"), mock.call("OK")])

    def test_log_task_error(self):
        mock_log_ok = mock.Mock()
        mock_log_err = mock.Mock()
        with self.assertRaises(ValueError):
            with log.LogTask("Testing", ok_logger=mock_log_ok,
                             err_logger=mock_log_err):
                raise ValueError("TestError")
        mock_log_ok.assert_called_once_with("Testing")
        mock_log_err.assert_called_once_with("FAILED")

    def test_create_logger(self):
        mock_log_ok = mock.Mock()
        mock_log_err = mock.Mock()

        def mock_get_logger(_):
            return type("MockLogger", (object,), dict(
                error=mock_log_err,
                info=mock_log_ok,
                setLevel=mock.Mock(),
                addHandler=mock.Mock()))

        def mock_logdir():
            return '/tmp'
        with mock.patch('logging.getLogger', mock_get_logger):
            with mock.patch('sett.utils.config.get_default_log_dir', mock_logdir()):
                logger = log.create_logger(__name__)
                with self.assertRaises(ValueError), logger.log_task("Testing"):
                    raise ValueError("TestError")
                mock_log_ok.assert_called_once_with("Testing")
                mock_log_err.assert_called_once_with("FAILED")
                self.assertTrue(hasattr(logger, "exception_to_message"))
