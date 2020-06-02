import unittest
from unittest.mock import patch

from sett.core import metadata
from sett.core.error import UserError


class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.dct = {
            "projectID": "Demo",
            "sender": "A"*32,
            "recipients": ["B"*256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A"*64,
            "checksum_algorithm": "SHA256",
            "compression_algorithm": "gzip",
            "version": "0.6"
        }

    def test_load_metadata(self):
        projects_by_id = {"Demo": object()}
        dct = self.dct
        with patch('sett.core.metadata.user_is_authorized_for_project',
                   lambda *_, **__: True):
            metadata.load_metadata(dct, projects_by_id)
            with self.assertRaises(UserError):
                metadata.load_metadata(dct, {})

        with patch('sett.core.metadata.user_is_authorized_for_project',
                   lambda *_, **__: False):
            with self.assertRaises(UserError):
                metadata.load_metadata(dct, projects_by_id)
