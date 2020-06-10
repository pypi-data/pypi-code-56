from __future__ import unicode_literals, absolute_import

import robosignatory.utils as utils
import robosignatory.work

import logging
log = logging.getLogger("robosignatory.atomicconsumer")


class AtomicSigner(object):

    def __init__(self, config):
        self.config = config
        self.signer = utils.get_signing_helper(**self.config["signing"])

        self.refs = {}
        for ref, val in self.config['ostree_refs'].items():
            if 'ref_to' in val:
                raise ValueError('ref_to in %s found. This is depricated' %
                                 ref)
            self.refs[ref] = val

        log.info('AtomicSigner ready for service')

    def consume(self, msg):
        # Example message:
        #  {u'ref': u'fedora-atomic/25/x86_64/docker-host',
        #   u'commitid': u'f99114401f....',
        #   u'arch': u'x86_64',
        #   u'variant': u'Atomic',
        #   u'location': u'http://kojipkgs....',
        #   u'compose_id': u'Fedora-25-20161002.n.0'}

        ref = msg.body['ref']
        commitid = msg.body['commitid']
        if commitid is None:
            return

        log.info('pungi composed %(ref)s (%(commitid)s, variant %(variant)s, '
                 'arch %(arch)s)' % msg.body)

        if ref not in self.refs:
            log.info('Unknown reference %s. Skipping' % ref)
            return

        val = self.refs[ref]

        robosignatory.work.process_atomic(self.signer, ref, commitid,
                                          **val)
