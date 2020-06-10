import unittest

from pytest import raises

import robosignatory.utils


class TestUtils(unittest.TestCase):

    def test_no_such_helper(self):
        with raises(KeyError):
            robosignatory.utils.get_signing_helper(backend='wat', )

    def test_get_sigul_helper(self):
        helper = robosignatory.utils.get_signing_helper(
            backend='sigul',
            user='ralph',
            passphrase_file='/tmp/wide-open.txt',
        )
        assert type(helper) == robosignatory.utils.SigulHelper

    def test_simple_echo_helper(self):
        helper = robosignatory.utils.get_signing_helper(
            backend='echo',
            user='ralph',
            passphrase_file='/tmp/wide-open.txt',
        )
        cmdline = helper.build_cmdline('wat')
        assert cmdline == ["echo", "build_cmdline: ('wat',) {}"]
