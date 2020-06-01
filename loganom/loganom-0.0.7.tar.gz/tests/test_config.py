"""Test for the Auxiliary functions"""

import unittest

from loganom.config import read_config


class TestConfig(unittest.TestCase):
    """Unittest for config.read_config()."""

    def test_config_sample(self):
        """Test for Read user configurations."""

        config_sample = 'config.ini.sample'
        result = read_config(config_sample)

        self.assertIsInstance(result)
