from __future__ import unicode_literals

import copy
import logging
import mock

import six
from fedora_messaging.api import Message
from pkg_resources import parse_version
from pytest import raises, mark, __version__ as pytest_version

from robosignatory.tag import TagSigner

try:
    import _pytest.logging
except ImportError:
    pass
else:
    if not hasattr(_pytest.logging.LogCaptureFixture, 'messages'):  # noqa
        # monkey-patch missing messages property
        class MyLogCaptureFixture(_pytest.logging.LogCaptureFixture):
            @property
            def messages(self):
                return [r.getMessage() for r in self.records]


requires_caplog = mark.skipif(
    parse_version(pytest_version) < parse_version("3.3.0"),
    reason="The caplog fixture was introduced in pytest 3.3.0"
)


TEST_CONFIG = {
    'signing': {
        'backend': 'echo',
    },
    'koji_instances': {
        'test': {
            'url': 'https://koji.example.com',
            'mbs_user': 'mbs_user',
            'options': {
                'authmethod': 'kerberos',
                'principal': 'test@EXAMPLE.COM',
            },
            'tags': [
                {
                    'from': 'f31-pending',
                    'to': 'f31',
                    'key': 'fedora-31',
                    'keyid': 'deadbeef',
                    'sidetags': {
                        'pattern': '<to>-build-side-<seq_id>',
                        'from': '<sidetag>-pending-signing',
                        'to': '<sidetag>-testing',
                        'trusted_taggers': ['bodhi'],
                    },
                },
                {
                    'from': 'f30-signing-pending',
                    'to': 'f30-updates-testing-pending',
                    'key': 'fedora-30',
                    'keyid': 'OU812I81B4U',
                    'type': 'plain',
                },
                {
                    'from': 'f30-modular-signing-pending',
                    'to': 'f30-modular-updates-testing-pending',
                    'key': 'fedora-30',
                    'keyid': 'OU812I81B4U',
                    'type': 'modular',
                }
            ],
        },
    },
    'ostree_refs': {},
    'coreos': {
        'bucket': 'testing',
        'key': 'testing',
        'aws': {
            'access_key': 'testing',
            'access_secret': 'testing',
            'region': 'us-east-1',
        }
    },
}


class MockUtils(mock.MagicMock):

    builds = [
        {'id': 1,
         'nvr': 'foo-1-1.fc31',
         'rpms': [
             {'id': 100,
              'nvr': 'foo-1-1.fc31',
              'arch': 'x64_64',
              'sigkey': '1234'},
             {'id': 101,
              'nvr': 'foo-libs-1-1.fc31',
              'arch': 'x64_64',
              'sigkey': '1234'},
         ]},
        {'id': 2,
         'nvr': 'bar-0.11-1.fc31',
         'rpms': [
             {'id': 200,
              'nvr': 'bar-0.11-1.fc31',
              'arch': 'x64_64',
              'sigkey': '2345'},
             {'id': 201,
              'nvr': 'bar-docs-0.11-1.fc31',
              'arch': 'noarch',
              'sigkey': '2345'},
         ]},
        {'id': 3,
         'nvr': 'gnu-10.0-5.fc31',
         'rpms': [
             {'id': 300,
              'nvr': 'gnu-10.0-5.fc31',
              'arch': 'x64_64'},
         ]},
    ]

    def _get_build(self, build_id):
        for b in self.builds:
            if b['id'] == build_id:
                return b

    def get_rpms(self, koji_client, build_nvr, build_id, sigkey=None):
        rpminfo = {}
        for rpm in self._get_build(build_id)['rpms']:
            info = {'id': rpm['id']}
            if sigkey:
                info['signed'] = rpm['sigkey'] == sigkey
            rpminfo['{}.{}'.format(rpm['nvr'], rpm['arch'])] = info
        return rpminfo

    def get_signing_helper(self, **signing_config):
        return mock.MagicMock(signing_config=signing_config)

    def run_command(self, cmdline):
        return 0, "", ""


class DummyContext(object):

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


@mock.patch(
    'robosignatory.consumer.fedora_messaging.config.conf',
    {'consumer_config': TEST_CONFIG}
)
class TestTagSigner(object):
    """Test the Koji tag signer class"""

    test_msg = {
        'topic': 'org.fedoraproject.prod.buildsys.tag',
        'body': {
            'name': 'foo', 'version': '1', 'release': '1.fc31',
            'build_id': 1, 'tag': 'f31-pending',
            'instance': 'test',
        },
    }

    def setup_method(self, method):
        # Patch in a mock koji session.
        with mock.patch('robosignatory.tag.koji.ClientSession') as self._koji_ClientSession:
            self.tag_signer = TagSigner(config=TEST_CONFIG)

        # Ensure methods can muck around with the test message contents and not
        # disturb each other.
        self.test_msg = copy.deepcopy(type(self).test_msg)

    @property
    def instance_obj(self):
        return self.tag_signer.koji_clients['test']

    @property
    def koji_client(self):
        return self.instance_obj['client']

    # Test creating the tag signer object with various (working & non-working)
    # configurations.

    def test_init(self):
        """Test that the tag signer can be created"""
        # The signer gets created in .setUp().

        assert self.instance_obj['mbs_user'] == 'mbs_user'

        self.koji_client.krb_login.assert_called_once_with(
            principal='test@EXAMPLE.COM')
        self.koji_client.ssl_login.assert_not_called()

    def test_init_with_ssl(self):
        """Test that a signer using SSL authentication can be created"""
        # We overwrite the signer here to inject non-standard configuration.
        test_config = copy.deepcopy(TEST_CONFIG)
        test_config['koji_instances']['test']['options'] = {
            'authmethod': 'ssl', 'cert': 'cert', 'serverca': 'serverca',
        }
        with mock.patch('robosignatory.tag.koji.ClientSession'):
            self.tag_signer = TagSigner(test_config)

        self.koji_client.ssl_login.assert_called_once_with(
            'cert', None, 'serverca')
        self.koji_client.krb_login.assert_not_called()

    def test_init_with_unknown_authmethod(self):
        """Test that unknown authmethods are caught"""
        # We overwrite the signer here to inject non-standard configuration.
        test_config = copy.deepcopy(TEST_CONFIG)
        test_config['koji_instances']['test']['options'] = {
            'authmethod': 'unknown'
        }
        with mock.patch(
            'robosignatory.tag.koji.ClientSession'
        ) as koji_client, raises(
            Exception, match='Only SSL and kerberos authmethods supported'
        ):
            self.tag_signer = TagSigner(test_config)

        koji_client.ssl_login.assert_not_called()
        koji_client.krb_login.assert_not_called()

    def test_init_with_duplicate_from_tag(self):
        """Test behavior with duplicate from tag"""
        # We overwrite the signer here to inject non-standard configuration.
        test_config = copy.deepcopy(TEST_CONFIG)
        tags = test_config['koji_instances']['test']['tags']
        tags.insert(1, tags[0])
        with mock.patch(
            'robosignatory.tag.koji.ClientSession'
        ), raises(
            Exception,
            match='From detected twice: {}'.format(tags[0]['from'])
        ):
            self.tag_signer = TagSigner(test_config)

    def test_init_with_unknown_tag_type(self):
        """Test behavior unknown tag type"""
        # We overwrite the signer here to inject non-standard configuration.
        test_config = copy.deepcopy(TEST_CONFIG)
        tags = test_config['koji_instances']['test']['tags']
        tags[0]['type'] = 'unknown'
        with mock.patch(
            'robosignatory.tag.koji.ClientSession'
        ), raises(
            Exception, match='Invalid tag type detected: unknown'
        ):
            self.tag_signer = TagSigner(test_config)

    # Test well-formed messages.

    def _prep_sidetag_test(self, sidetag_pending, error):
        tags_key = self.test_msg['body']['tag']  # normal tag where we find robosig configuration
        tag_conf = self.instance_obj['tags'][tags_key]

        for sidetag_conf in self.instance_obj['sidetags'].values():
            if sidetag_conf['tags_key'] == tags_key:
                tag_conf['sidetags'] = sidetag_conf
                break
        else:
            raise RuntimeError("Can't find sidetag configuration for {}".format(
                tag_conf['from']))

        if error == 'untrusted-tagger':
            tagger = 'hamburglar'
        else:
            tagger = 'bodhi'

        if error == 'missing-from-history':
            tag_history = []
        else:
            tag_history = [
                {'active': True,
                 'create_ts': 1554076800,
                 'creator_name': tagger,
                 'tag_name': sidetag_pending},
            ]
        self.koji_client.tagHistory.return_value = tag_history

        return tag_conf, tagger

    def _get_expected_messages_and_exceptions(self, sidetag_pending, error,
                                              build_owner, tag_conf, tagger):
        body = self.test_msg['body']
        instance = body['instance']
        build_nvr = '{name}-{version}-{release}'.format(**body)
        from_tag = body['tag']
        build_id = body['build_id']

        expected_log_msgs = [
            "Build {} ({}) tagged into {} on {}".format(
                build_nvr, build_id, from_tag, instance),
        ]

        if error == 'non-mbs-owner':
            expected_log_msgs.append(
                "Build {} has owner {}, which is NOT mbs_user!".format(build_id, build_owner))
            expected_exc_ctx = raises(Exception,
                                      match="Modular content tag contains invalid owned build")
        elif error == 'untrusted-tagger':
            expected_log_msgs.append(
                "Side tag build not tagged into {} by trusted user ({}) but by '{}'!".format(
                    sidetag_pending, ", ".join(tag_conf['sidetags']['trusted_taggers']), tagger
                )
            )
            expected_exc_ctx = raises(Exception,
                                      match="Side tag build tagged by untrusted user")
        elif error == 'missing-from-history':
            expected_log_msgs.append(
                "Couldn't find tag {} in history of build {} ({})!".format(
                    sidetag_pending, build_nvr, build_id
                )
            )
            expected_exc_ctx = raises(Exception,
                                      match="Tag not found in build history")
        else:
            expected_exc_ctx = DummyContext()

        return expected_log_msgs, expected_exc_ctx

    @requires_caplog
    @mock.patch('robosignatory.tag.utils', new_callable=MockUtils())
    @mark.parametrize(
        'type_,sidetag_pending,error',
        ((None, None, None),
         ('plain', None, None),
         ('plain', 'f31-build-side-1234-pending-signing', None),
         ('plain', 'f31-build-side-1234-pending-signing', 'untrusted-tagger'),
         ('plain', 'f31-build-side-1234-pending-signing', 'missing-from-history'),
         ('modular', None, None),
         ('modular', None, 'non-mbs-owner')))
    def test_build_messages(self, utils, caplog, type_, sidetag_pending, error):
        """Test build messages for various types."""
        caplog.set_level(logging.DEBUG)

        body = self.test_msg['body']
        build_nvr = '{name}-{version}-{release}'.format(**body)
        from_tag = body['tag']
        build_id = body['build_id']
        tag_conf = self.instance_obj['tags'][from_tag]
        to_tag = tag_conf['to']
        tagger = None
        build_owner = None

        if type_ == 'modular':
            body['tag'] = from_tag = 'f30-modular-signing-pending'
            to_tag = 'f30-modular-updates-testing-pending'
            if error == 'non-mbs-owner':
                build_owner = 'hamburglar'
            else:
                build_owner = TEST_CONFIG['koji_instances']['test']['mbs_user']

            self.koji_client.listTagged.return_value = [
                {'owner_name': build_owner, 'nvr': build_nvr, 'build_id': build_id}
            ]

        if sidetag_pending:
            tag_conf, tagger = self._prep_sidetag_test(sidetag_pending, error)
            body['tag'] = from_tag = sidetag_pending
            to_tag = sidetag_pending.replace('-pending-signing', '-testing')

        expected_log_msgs, expected_exc_ctx = self._get_expected_messages_and_exceptions(
            sidetag_pending, error, build_owner, tag_conf, tagger
        )

        msg = Message(**self.test_msg)
        with expected_exc_ctx:
            self.tag_signer.consume(msg)

        # Equivalent to caplog.messages but compatible with pytest < 3.7
        logged_messages = [record.getMessage() for record in caplog.records]

        for msg in expected_log_msgs:
            assert msg in logged_messages

        if not error:
            self.koji_client.tagBuild.assert_called_once_with(to_tag, build_id,
                                                              False, from_tag)
        else:
            self.koji_client.tagBuild.assert_not_called()

    @requires_caplog
    def test_plain_build_message_with_unconfigured_tag(self, caplog):
        """Test the behavior with an unconfigured tag"""
        caplog.set_level(logging.DEBUG)

        self.test_msg['body']['tag'] = 'unconfigured'
        msg = Message(**self.test_msg)
        self.tag_signer.consume(msg)

        # Equivalent to caplog.messages but compatible with pytest < 3.7
        logged_messages = [record.getMessage() for record in caplog.records]

        assert "Tag not autosigned, skipping" in logged_messages

        self.koji_client.tagBuild.assert_not_called()

    # Test invalid messages.

    @mock.patch('robosignatory.tag.log')
    def test_unknown_koji_instance(self, log):
        """Test an unknown Koji instance in the message"""
        self.test_msg['body']['instance'] = 'unknown'
        msg = Message(**self.test_msg)
        self.tag_signer.consume(msg)

        log.info.assert_called_with('Koji instance not known, skipping')

    @mark.skipif(not six.PY2, reason="only relevant on Python 2")
    def test_py2_koji_client_args(self):
        assert self._koji_ClientSession.call_count == 1
        assert not isinstance(self._koji_ClientSession.call_args_list[0][0][0], unicode)
        for kwarg, value in self._koji_ClientSession.call_args_list[0][1].items():
            assert not isinstance(value, unicode)

    @mark.skipif(not six.PY2, reason="only relevant on Python 2")
    def test_py2_krb_login_args(self):
        assert self.instance_obj["client"].krb_login.call_count == 1
        assert not isinstance(
            self.instance_obj["client"].krb_login.call_args_list[0][1]["principal"],
            unicode
        )
