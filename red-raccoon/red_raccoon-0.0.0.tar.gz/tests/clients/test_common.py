import red_raccoon.cli.common
import unittest


class CLIHelperTestCases(unittest.TestCase):
    def test_arg_as_set(self):
        for vector, expected in [
            ('*cred*', {'*cred*'}),
            ('credential access', {'credential access'}),
            ('credential access,lateral movement', {'credential access', 'lateral movement'})
        ]:
            with self.subTest(vector):
                result = red_raccoon.cli.common.arg_as_set(vector)
                self.assertSetEqual(expected, result)
