import unittest
from unittest import mock

from sett.protocols import multipart


class TestMultipart(unittest.TestCase):
    def test_encode(self):
        with mock.patch("uuid.uuid4", lambda: type("mockuuid", (object,), {"hex": "UUID"})):
            self.assertEqual(
                multipart.encode("Filedata", "data.tar", b".........",
                                 extra_data=(("a", "AAA"), ("b", "BBB"))),
                ("multipart/form-data; boundary=UUID",
                 b'--UUID\r\n'
                 b'Content-Disposition: form-data; name="a"\r\n\r\nAAA'
                 b'\r\n'
                 b'--UUID\r\n'
                 b'Content-Disposition: form-data; name="b"\r\n\r\nBBB'
                 b'\r\n'
                 b'--UUID\r\n'
                 b'Content-Disposition: form-data; name="Filedata"; filename="data.tar"\r\n'
                 b'Content-Type: application/x-tar\r\n'
                 b'\r\n'
                 b'.........'
                 b'\r\n--UUID--\r\n'
                 )
            )
            self.assertEqual(
                multipart.encode("Filedata", "data.tar", b"........."),
                ("multipart/form-data; boundary=UUID",
                 b'--UUID\r\n'
                 b'Content-Disposition: form-data; name="Filedata"; filename="data.tar"\r\n'
                 b'Content-Type: application/x-tar\r\n'
                 b'\r\n'
                 b'.........'
                 b'\r\n--UUID--\r\n'
                 )
            )
