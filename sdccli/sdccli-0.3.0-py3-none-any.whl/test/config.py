import os
import os.path
import unittest

from unittest.mock import patch
from sdccli.config import Config


config_path = os.path.join(os.path.dirname(__file__), "assets", "config.yml")
monitor_url = 'https://app.sysdigcloud.com'
secure_url = 'https://secure.sysdig.com'

def load_config():
    conf = Config()
    conf.load(path=config_path)
    return conf


class TestConfig(unittest.TestCase):

    def test_main(self):
        conf = load_config()
        self.assertEqual(conf.monitor['token'], 'monitor-token')
        self.assertEqual(conf.monitor['url'], monitor_url)
        self.assertTrue(conf.monitor['ssl_verify'])

        self.assertEqual(conf.secure['token'], 'secure-token')
        self.assertEqual(conf.secure['url'], secure_url)
        self.assertTrue(conf.secure['ssl_verify'])

    def test_example(self):
        conf = Config()
        conf.load(path=config_path, env="example")

        self.assertEqual(conf.monitor['token'], 'monitor-example-token')
        self.assertEqual(conf.monitor['url'], 'https://monitor.example.com')
        self.assertFalse(conf.monitor['ssl_verify'])

        self.assertEqual(conf.secure['token'], 'secure-example-token')
        self.assertEqual(conf.secure['url'], 'https://secure.example.com')
        self.assertTrue(conf.secure['ssl_verify'])

    def test_env_token(self):
        token = 'new-token'
        with patch.dict('os.environ', {'SDC_TOKEN': token}):
            conf = load_config()
            self.assertEqual(conf.monitor['token'], token)
            self.assertEqual(conf.secure['token'], token)

        with patch.dict('os.environ', {'SDC_MONITOR_TOKEN': token}):
            conf = load_config()
            self.assertEqual(conf.monitor['token'], token)
            self.assertEqual(conf.secure['token'], 'secure-token')

        with patch.dict('os.environ', {'SDC_SECURE_TOKEN': token}):
            conf = load_config()
            self.assertEqual(conf.monitor['token'], 'monitor-token')
            self.assertEqual(conf.secure['token'], token)

    def test_env_env(self):
        with patch.dict('os.environ', {'SDC_ENV': 'example'}):
            conf = load_config()
            self.assertEqual(conf.monitor['url'], 'https://monitor.example.com')

    def test_env_url(self):
        url = 'https://new.example.com'
        with patch.dict('os.environ', {'SDC_MONITOR_URL': url}):
            conf = load_config()
            self.assertEqual(conf.monitor['url'], url)
            self.assertEqual(conf.secure['url'], secure_url)

        with patch.dict('os.environ', {'SDC_SECURE_URL': url}):
            conf = load_config()
            self.assertEqual(conf.monitor['url'], monitor_url)
            self.assertEqual(conf.secure['url'], url)
