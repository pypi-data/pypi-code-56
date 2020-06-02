import unittest
from unittest import mock

from sett.protocols import sftp


class TestSftp(unittest.TestCase):
    def setUp(self):
        sftp_client = mock.Mock()
        sftp_client.put = mock.Mock()

        class MockTransport:
            connect = mock.Mock()
            auth_interactive = mock.Mock()
            open_sftp_client = mock.Mock(return_value=sftp_client)
            close = mock.Mock()
            @staticmethod
            def auth_publickey(*_, **__):
                raise sftp.SSHException("Access Denied")
        self.transport = mock.Mock(return_value=MockTransport)
        self.MockTransport = MockTransport
        self.sftp_client = sftp_client

    def test_sftp_connection(self):
        with mock.patch("sett.protocols.sftp.Transport",
                        self.transport), \
            mock.patch("sett.protocols.sftp.auth_handler",
                       "handler"):
            with sftp.sftp_connection("host", "user",
                                      two_factor_callback=None) as connection:
                connection.put("localpath", "remotepath",
                               "callback", "confirm")
        self.transport.assert_called_once_with("host")
        self.MockTransport.connect.assert_called_once_with()
        self.MockTransport.auth_interactive.assert_called_once_with(
            "user", "handler")
        self.MockTransport.open_sftp_client.assert_called_once_with()
        self.sftp_client.assert_not_called()
        self.sftp_client.put.assert_called_once_with("localpath", "remotepath",
                                                     "callback", "confirm")
        self.sftp_client.close.assert_called_once_with()
        self.MockTransport.close.assert_called_once_with()

    def test_sftp_connection_fail(self):
        with mock.patch("sett.protocols.sftp.Transport",
                        self.transport), \
            mock.patch("sett.protocols.sftp.auth_handler",
                       "handler"):
            with self.assertRaises(ValueError):
                with sftp.sftp_connection("host", "user",
                                          two_factor_callback=None):
                    raise ValueError("Test Error")
        self.transport.assert_called_once_with("host")
        self.MockTransport.connect.assert_called_once_with()
        self.MockTransport.auth_interactive.assert_called_once_with(
            "user", "handler")
        self.MockTransport.open_sftp_client.assert_called_once_with()
        self.sftp_client.assert_not_called()
        self.sftp_client.put.assert_not_called()
        self.sftp_client.close.assert_called_once_with()
        self.MockTransport.close.assert_called_once_with()
