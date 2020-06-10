import os
import unittest
import copy
from collections import namedtuple

import mock
from botocore.exceptions import ClientError
from fedora_messaging.api import Message
from fedora_messaging.testing import mock_sends

from robosignatory.coreos import CoreOSSigner


TEST_CONFIG = {
    "signing": {
        "backend": "echo",
    },
    "koji_instances": {},
    "ostree_refs": {},
    "coreos": {
        "bucket": "testing",
        "key": "testing",
        "aws": {
            "access_key": "testing",
            "access_secret": "testing",
            "region": "us-east-1",
        }
    },
}

ARTIFACTS_MESSAGE = Message(
    topic="org.fedoraproject.prod.coreos.build.request.artifacts-sign",
    body={
        "build_id": "buildid",
        "basearch": "basearch",
        "artifacts": [{
            "file": "s3://host/some/path/test1",
            "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        }]
    }
)

OSTREE_MESSAGE = Message(
    topic="org.fedoraproject.prod.coreos.build.request.ostree-sign",
    body={
        "build_id": "buildid",
        "basearch": "basearch",
        "commit_object": "s3://host/some/path/test1",
        "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    }
)

S3Object = namedtuple("S3Object", "size")

def fake_download(source, local):
    open(local, "w").close()

def fake_download_and_artifact_sign(source, local):
    fake_download(source, local)
    # Also create the sig file for testing
    open(local + ".sig", "w").close()

def fake_download_and_ostree_sign(source, local):
    fake_download(source, local)
    # Also create the sig file for testing
    open(os.path.dirname(local) + "/ostree-commitmeta-object", "w").close()


class TestCoreOS(unittest.TestCase):

    def setUp(self):
        self.consumer = CoreOSSigner(TEST_CONFIG)
        self.consumer.bucket = mock.Mock()

    def _get_response_message(self, source_msg, failed=False, failure_msg=""):
        body = dict(source_msg.body)
        body.update({"status": "FAILURE" if failed else "SUCCESS"})
        if failed:
            body.update({"failure-message": failure_msg})
        return Message(
            topic=source_msg.topic + ".finished",
            body=body
        )

    @mock.patch('robosignatory.coreos.utils.run_command')
    def test_artifacts_sign(self, run_command):
        self.consumer.bucket.download_file.side_effect = fake_download_and_artifact_sign
        run_command.return_value = 0, "", ""
        self.consumer.bucket.objects.filter.return_value = [S3Object(size=0)]
        expected_response = self._get_response_message(ARTIFACTS_MESSAGE)

        with mock_sends(expected_response):
            self.consumer.consume(ARTIFACTS_MESSAGE)

        self.consumer.bucket.download_file.assert_called()
        assert self.consumer.bucket.download_file.call_args_list[0][0][0] == "some/path/test1"
        run_command.assert_called()
        self.consumer.bucket.upload_file.assert_called()
        assert self.consumer.bucket.upload_file.call_args_list[0][0][1] == "some/path/test1.sig"

    @mock.patch('robosignatory.coreos.utils.run_command')
    def test_ostree_sign(self, run_command):
        self.consumer.bucket.download_file.side_effect = fake_download_and_ostree_sign
        run_command.return_value = 0, "", ""
        self.consumer.bucket.objects.filter.return_value = [S3Object(size=0)]
        expected_response = self._get_response_message(OSTREE_MESSAGE)

        with mock_sends(expected_response):
            self.consumer.consume(OSTREE_MESSAGE)

        self.consumer.bucket.download_file.assert_called()
        assert self.consumer.bucket.download_file.call_args_list[0][0][0] == "some/path/test1"
        run_command.assert_called()
        self.consumer.bucket.upload_file.assert_called()
        assert self.consumer.bucket.upload_file.call_args_list[0][0][1] == "some/path/ostree-commitmeta-object"

    @mock.patch('robosignatory.coreos.utils.run_command')
    def test_wrong_checksum(self, run_command):
        new_body = copy.deepcopy(ARTIFACTS_MESSAGE.body)
        new_body["artifacts"][0]["checksum"] = "sha256:wrong-checksum"
        msg = Message(topic=ARTIFACTS_MESSAGE.topic, body=new_body)
        self.consumer.bucket.download_file.side_effect = fake_download
        expected_response = self._get_response_message(msg, failed=True,
            failure_msg='Incorrect SHA256 for some/path/test1, not signing')

        with mock_sends(expected_response):
            self.consumer.consume(msg)

        self.consumer.bucket.download_file.assert_called()
        run_command.assert_not_called()
        self.consumer.bucket.upload_file.assert_not_called()

    @mock.patch('robosignatory.coreos.utils.run_command')
    def test_signing_failed(self, run_command):
        self.consumer.bucket.download_file.side_effect = fake_download
        run_command.return_value = 1, "stdout", "stderr"
        expected_response = self._get_response_message(
            ARTIFACTS_MESSAGE, failed=True,
            failure_msg='Error signing! Signing output: 1, stdout: stdout, stderr: stderr')

        with mock_sends(expected_response):
            self.consumer.consume(ARTIFACTS_MESSAGE)

        self.consumer.bucket.download_file.assert_called()
        run_command.assert_called()
        self.consumer.bucket.upload_file.assert_not_called()

    @mock.patch('robosignatory.coreos.utils.run_command')
    def test_no_signature(self, run_command):
        self.consumer.bucket.download_file.side_effect = fake_download
        run_command.return_value = 0, "stdout", "stderr"
        expected_response = self._get_response_message(
            ARTIFACTS_MESSAGE, failed=True,
            failure_msg='Signer did not produce any signature file for some/path/test1')

        with mock_sends(expected_response):
            self.consumer.consume(ARTIFACTS_MESSAGE)

        self.consumer.bucket.download_file.assert_called()
        run_command.assert_called()
        self.consumer.bucket.upload_file.assert_not_called()

    def test_download_failed(self):
        self.consumer.bucket.download_file.side_effect = ClientError({}, None)
        expected_response = self._get_response_message(
            ARTIFACTS_MESSAGE, failed=True,
            failure_msg='Could not download some/path/test1: An error occurred '
                        '(Unknown) when calling the None operation: Unknown')

        with mock_sends(expected_response):
            self.consumer.consume(ARTIFACTS_MESSAGE)

        self.consumer.bucket.download_file.assert_called()
        self.consumer.bucket.upload_file.assert_not_called()

    def test_key_parse_config(self):
        # Verify that when a key is provided via the config it is used
        consumer = CoreOSSigner(TEST_CONFIG)
        msg = Message(topic=ARTIFACTS_MESSAGE.topic, body=ARTIFACTS_MESSAGE.body)
        self.assertEqual(consumer.get_key(msg), "testing")

    def test_key_parse_autodetect(self):
        # Verify that when no key is provided via the config the key
        # is autodetected.
        # 
        # Grab the config and remove the hardcoded key to enable auto detection
        config = copy.deepcopy(TEST_CONFIG)
        del config["coreos"]["key"]
        consumer = CoreOSSigner(config)
        # Grab the message body and set the build_id to a version number
        new_body = copy.deepcopy(ARTIFACTS_MESSAGE.body)
        new_body["build_id"] = "32.20200601.2.1"
        # Process the Message and verify the key matches what we expect
        msg = Message(topic=ARTIFACTS_MESSAGE.topic, body=new_body)
        self.assertEqual(consumer.get_key(msg), "fedora-32")
