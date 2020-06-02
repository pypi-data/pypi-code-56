import unittest
import json

from httmock import urlmatch, HTTMock
from click.testing import CliRunner
from sdccli.cli import cli


class TestScanningImage(unittest.TestCase):
    def setUp(self):
        pass

    def mock(self, ret):
        @urlmatch(path='/api/scanning/v1/anchore/images')
        def response(url, request):
            self.url = url
            self.request = request
            return json.dumps(ret)
        return HTTMock(response)

    def test_list(self):
        with self.mock([image_old, image]):
            runner = CliRunner()
            result = runner.invoke(cli, ['scanning', 'image', 'list'])
        self.assertEqual(result.exit_code, 0)
        self.assertFalse(image_old['image_detail'][0]['imageId'] in result.output)
        self.assertTrue(image_id in result.output)

    def test_show_all(self):
        with self.mock([image_old, image]):
            runner = CliRunner()
            result = runner.invoke(cli, ['scanning', 'image', 'list', '--show-all'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(image_old['image_detail'][0]['imageId'] in result.output)
        self.assertTrue(image_id in result.output)

    def test_get(self):
        with self.mock([image]):
            runner = CliRunner()
            result = runner.invoke(cli, ['scanning', 'image', 'get', fulltag])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(image['image_detail'][0]['repo'] in self.url.query)
        self.assertFalse(image_old['image_detail'][0]['imageId'] in result.output)
        self.assertTrue(image_id in result.output)

    def test_add(self):
        with self.mock([image]):
            runner = CliRunner()
            result = runner.invoke(cli, ['scanning', 'image', 'add', fulltag])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.request.method, 'POST')
        self.assertTrue(fulltag in self.request.body)
        self.assertFalse(image_old['image_detail'][0]['imageId'] in result.output)
        self.assertTrue(image_id in result.output)

    def test_del(self):
        with self.mock([image]):
            runner = CliRunner()
            result = runner.invoke(cli, ['scanning', 'image', 'del', fulltag])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.request.method, 'DELETE')
        self.assertTrue(image_id in self.url.path)

    def test_content_empty(self):
        with self.mock(["os", "files", "npm", "gem", "python", "java"]):
            runner = CliRunner()
            result = runner.invoke(cli, ['scanning', 'image', 'content', digest])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(image_id in self.url.path)
        self.assertTrue("gem" in result.output)

    def test_content_os(self):
        with self.mock(content_os):
            runner = CliRunner()
            result = runner.invoke(cli, ['scanning', 'image', 'content', digest, 'os'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(image_id in self.url.path)
        for c in content_os['content']:
            self.assertTrue(c['package'] in result.output)


image_old = {
    "analysis_status": "analyzed",
    "analyzed_at": "2019-06-17T00:02:49Z",
    "annotations": {},
    "created_at": "2019-06-17T00:02:14Z",
    "imageDigest": "sha256:aaaaaa",
    "image_content": {
        "metadata": {
            "arch": "amd64",
            "distro": "foobar",
            "distro_version": "1.0.0",
            "dockerfile_mode": "Guessed",
            "image_size": 10769712,
            "layer_count": 20
        }
    },
    "image_detail": [
        {
            "created_at": "2019-06-17T00:02:14Z",
            "digest": "sha256:aaaaaa",
            "dockerfile": "",
            "userId": "tenant_12345",
            "imageId": "aaaaaa",
            "registry": "docker.io",
            "repo": "foobar",
            "tag": "latest",
            "fulltag": "docker.io/foobar:latest"
        }
    ],
    "image_status": "active",
    "image_type": "docker",
    "last_updated": "2019-06-17T00:02:49Z",
    "parentDigest": "sha256:aaaaaa",
    "userId": "tenant_12345"
}

image = {
    "analysis_status": "analyzed",
    "analyzed_at": "2019-06-17T00:02:49Z",
    "annotations": {},
    "created_at": "2019-06-17T00:02:14Z",
    "imageDigest": "sha256:bbbbbb",
    "image_content": {
        "metadata": {
            "arch": "amd64",
            "distro": "foobar",
            "distro_version": "2.0.0",
            "dockerfile_mode": "Guessed",
            "image_size": 10769712,
            "layer_count": 20
        }
    },
    "image_detail": [
        {
            "created_at": "2019-06-17T00:02:14Z",
            "digest": "sha256:bbbbbb",
            "dockerfile": "",
            "userId": "tenant_12345",
            "imageId": "bbbbbb",
            "registry": "docker.io",
            "repo": "foobar",
            "tag": "latest",
            "fulltag": "docker.io/foobar:latest"
        }
    ],
    "image_status": "active",
    "image_type": "docker",
    "last_updated": "2019-06-17T00:02:49Z",
    "parentDigest": "sha256:bbbbbb",
    "userId": "tenant_12345"
}

fulltag = image['image_detail'][0]['fulltag']
image_id = image['image_detail'][0]['imageId']
digest = image['image_detail'][0]['digest']


content_os = {
    "content": [
        {
            "license": "GPL-2.0",
            "origin": "foo bar <foobar@example.com>",
            "package": "my_package",
            "size": "409600",
            "type": "APKG",
            "version": "3.1.0"
        }
    ]
}
