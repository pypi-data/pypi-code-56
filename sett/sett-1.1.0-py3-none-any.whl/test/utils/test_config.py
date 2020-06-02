import unittest
from unittest.mock import patch
import json
import dataclasses

from sett.utils import config
from sett.core.error import UserError
from sett.core.model import Project


class TestConfig(unittest.TestCase):
    @staticmethod
    def test_default_config_serializable():
        json.dumps(dataclasses.asdict(config.default_config()))


class TestLoadProjects(unittest.TestCase):
    @patch("sett.utils.config.urlopen")
    def test_data_ok(self, mock_urlopen):
        data = [{"name": "Project One",
                 "project_id": "project1"
                 },
                {"name": "Project Two",
                 "project_id": "project2"
                 }]
        response = mock_urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps(data).encode()
        projects = config.load_projects(config.default_config())
        self.assertListEqual(projects,
                             [Project(**project) for project in data])

    @patch("sett.utils.config.urlopen")
    def test_data_wrong(self, mock_urlopen):
        wrong_content = [b"[{}]",
                         b'[{"foo": "Project One", "bar": "project1"}]',
                         b"wrong format"]
        for data in wrong_content:
            response = mock_urlopen.return_value.__enter__.return_value
            response.read.return_value = data
            with self.assertRaises(UserError):
                config.load_projects(config.default_config())
