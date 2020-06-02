import unittest
import json

from httmock import urlmatch, HTTMock
from click.testing import CliRunner
from sdccli.cli import cli


class TestEvent(unittest.TestCase):
    def setUp(self):
        pass

    def mock(self, ret):
        @urlmatch(path='/api/events/')
        def response(url, request):
            self.url = url
            self.request = request
            self.result = json.dumps(ret)
            return json.dumps(ret)
        return HTTMock(response)

    def test_list(self):
        with self.mock({
            "total": 2,
            "offset": 0,
            "events": [event1, event2]
        }):
            runner = CliRunner()
            result = runner.invoke(cli, ['event', 'list'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(event1["name"] in result.output)
        self.assertTrue(event2["name"] in result.output)

    def test_get(self):
        with self.mock({
            "total": 2,
            "offset": 0,
            "events": [event1, event2]
        }):
            runner = CliRunner()
            result = runner.invoke(cli, ['event', 'get', event1["name"]])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.request.method, 'GET')
        self.assertTrue(event1["name"] in result.output)
        self.assertFalse(event2["name"] in result.output)

    def test_delete(self):
        with self.mock({}):
            runner = CliRunner()
            result = runner.invoke(cli, ['event', 'del', event1["id"]])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.request.method, 'DELETE')
        self.assertTrue(event1["id"] in self.url.path)

    def test_add(self):
        with self.mock({
            "event": event1
        }):
            runner = CliRunner()
            result = runner.invoke(cli, [
                'event', 'add', '--description', event1["description"], '--severity', 7, event1["name"]])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.request.method, 'POST')
        self.assertTrue(event1["name"] in result.output)
        self.assertFalse(event2["name"] in result.output)


event1 = {
    "id": "1111111",
    "version": 1,
    "severityLabel": "LOW",
    "name": "event1",
    "description": "event 1",
    "timestamp": 1500000000000,
    "tags": {
        "ConatinerID": "fabafaba0001",
        "source": "docker",
    },
    "repository": "docker.io/alpine",
    "imageTag": "3.0",
    "digest": "sha256:001",
    "type": "SCANNING"
}


event2 = {
    "id": "2222222",
    "version": 1,
    "severityLabel": "MEDIUM",
    "name": "event2",
    "description": "event 2",
    "timestamp": 1550000000000,
    "tags": {
        "ConatinerID": "fabafaba0002",
        "source": "docker",
    },
    "repository": "docker.io/alpine",
    "imageTag": "3.2",
    "digest": "sha256:002",
    "type": "SCANNING"
}
