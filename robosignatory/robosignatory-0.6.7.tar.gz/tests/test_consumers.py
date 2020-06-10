import unittest

from fedora_messaging.api import Message
from fedora_messaging.exceptions import Nack
import mock

from robosignatory.consumer import Consumer


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


@mock.patch(
    "robosignatory.consumer.fedora_messaging.config.conf",
    {"consumer_config": TEST_CONFIG}
)
class TestConsumers(unittest.TestCase):

    @mock.patch('robosignatory.consumer.TagSigner')
    def test_message_tag(self, Handler):
        msg = Message(
            topic="org.fedoraproject.prod.buildsys.tag",
            body={}
        )
        consumer = Consumer()
        consumer.tag_handler = mock.Mock()
        consumer(msg)
        consumer.tag_handler.consume.assert_called_once_with(msg)

    @mock.patch('robosignatory.consumer.AtomicSigner')
    def test_message_atomic(self, Handler):
        msg = Message(
            topic="org.fedoraproject.prod.pungi.compose.ostree",
            body={}
        )
        consumer = Consumer()
        consumer.atomic_handler = mock.Mock()
        consumer(msg)
        consumer.atomic_handler.consume.assert_called_once_with(msg)

    @mock.patch('robosignatory.consumer.CoreOSSigner')
    def test_message_coreos_artifacts_sign(self, Handler):
        msg = Message(
            topic="org.fedoraproject.prod.coreos.build.request.artifacts-sign",
            body={}
        )
        consumer = Consumer()
        consumer.coreos_handler = mock.Mock()
        consumer(msg)
        consumer.coreos_handler.consume.assert_called_once_with(msg)

    @mock.patch('robosignatory.consumer.CoreOSSigner')
    def test_message_coreos_ostree_sign(self, Handler):
        msg = Message(
            topic="org.fedoraproject.prod.coreos.build.request.ostree-sign",
            body={}
        )
        consumer = Consumer()
        consumer.coreos_handler = mock.Mock()
        consumer(msg)
        consumer.coreos_handler.consume.assert_called_once_with(msg)

    @mock.patch('robosignatory.consumer.log.exception')
    def test_message_exception(self, error):
        """Test catching an exception when processing messages."""
        msg = mock.Mock()
        # Ensure msg.topic.endswith() throws an exception right away, this way
        # we can forgo mocking out handlers or similar complications.
        msg.topic = None

        with self.assertRaises(Nack) as exc:
            Consumer()(msg)

        msg = ("'NoneType' object has no attribute 'endswith': "
               "Unable to handle message: {}".format(msg))
        error.assert_called_once_with(msg)
        self.assertEqual(str(exc.exception), msg)
