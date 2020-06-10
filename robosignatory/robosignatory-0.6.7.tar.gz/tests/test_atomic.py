import unittest
import copy

import mock
from fedora_messaging.api import Message

from robosignatory.atomic import AtomicSigner


TEST_CONFIG = {
    "signing": {
        "backend": "echo",
    },
    "koji_instances": {},
    "ostree_refs": {
        "fedora-atomic/25/x86_64/docker-host": {
            "directory": "/mnt/koji/compose/atomic/25/",
            "key": "fedora-25",
        },
        "fedora/devel/armhfp/iot": {
            "directory": "/mnt/koji/compose/iot/repo/",
            "key": "fedora-31",
        },
    },
}

IOT_MESSAGE = Message(
    topic="org.fedoraproject.prod.pungi.compose.ostree",
    body={
        "arch": "armhfp",
        "commitid": "deadbeef",
        "compose_date": "20191011",
        "compose_id": "Fedora-IoT-31-20191011.0",
        "compose_label": "RC-20191011.0",
        "compose_respin": 0,
        "compose_type": "production",
        "local_repo_path": "/mnt/koji/compose/iot/repo/",
        "location":
            "http://kojipkgs.fedoraproject.org/compose/iot/Fedora-IoT-31-20191011.0/compose",
        "ref": "fedora/devel/armhfp/iot",
        "release_is_layered": False,
        "release_name": "Fedora-IoT",
        "release_short": "Fedora-IoT",
        "release_type": "ga",
        "release_version": "31",
        "repo_path": "http://kojipkgs.fedoraproject.org/compose/iot/repo",
        "variant": "IoT",
    }
)


class TestAtomic(unittest.TestCase):

    def setUp(self):
        self.consumer = AtomicSigner(TEST_CONFIG)

    @mock.patch('robosignatory.work.process_atomic')
    def test_iot_sign(self, process_atomic):
        self.consumer.consume(IOT_MESSAGE)
        process_atomic.assert_called_with(
            self.consumer.signer,
            'fedora/devel/armhfp/iot',
            'deadbeef',
            directory='/mnt/koji/compose/iot/repo/',
            key='fedora-31',
        )

    @mock.patch('robosignatory.work.process_atomic')
    def test_no_commitid(self, process_atomic):
        msg = Message(topic=IOT_MESSAGE.topic, body=copy.deepcopy(IOT_MESSAGE.body))
        msg.body["commitid"] = None
        self.consumer.consume(msg)
        process_atomic.assert_not_called()

