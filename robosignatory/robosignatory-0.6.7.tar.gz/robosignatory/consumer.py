from __future__ import unicode_literals, absolute_import

import logging

import fedora_messaging

from .tag import TagSigner
from .atomic import AtomicSigner
from .coreos import CoreOSSigner


log = logging.getLogger('robosignatory')


class Consumer(object):
    """All messages are received by this class's __call__() method."""

    def __init__(self):
        log.info('Initializing Robosignatory consumer')
        self.config = fedora_messaging.config.conf["consumer_config"]
        self.tag_handler = TagSigner(self.config)
        self.atomic_handler = AtomicSigner(self.config)
        self.coreos_handler = CoreOSSigner(self.config)

    def __call__(self, msg):
        """
        Callback method called by fedora-messaging consume.

        Redirect messages to the correct handler using the
        message topic.

        In case of duplicate messages, robosignatory will just try to re-sign
        the object, which will have no effect (except wasted cyles but that
        should not be a major problem).

        Args:
            msg (fedora_messaging.api.Message): The message received from the broker.
        """
        log.info('Received message from fedora-messaging with topic: %s', msg.topic)

        try:
            if msg.topic.endswith('.buildsys.tag'):
                log.debug('Passing message to the Tag handler')
                self.tag_handler.consume(msg)
            elif msg.topic.endswith('.pungi.compose.ostree'):
                log.debug('Passing message to the Atomic handler')
                self.atomic_handler.consume(msg)
            elif (msg.topic.endswith('.coreos.build.request.artifacts-sign')
                  or msg.topic.endswith('.coreos.build.request.ostree-sign')):
                log.debug('Passing message to the CoreOS handler')
                self.coreos_handler.consume(msg)
        except Exception as e:
            error_msg = '{e}: Unable to handle message: {msg}'.format(e=e, msg=msg)
            log.exception(error_msg)
            raise fedora_messaging.exceptions.Nack(error_msg)
