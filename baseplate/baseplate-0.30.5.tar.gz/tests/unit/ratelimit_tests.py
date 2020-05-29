from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from baseplate import ratelimit
from baseplate.ratelimit.backends import RateLimitBackend
from baseplate.ratelimit.backends.redis import RedisRateLimitBackend
from baseplate.ratelimit.backends.memcache import MemcacheRateLimitBackend
from pymemcache.client.base import PooledClient
from redis import StrictRedis

from .. import mock


class MockRateLimitBackend(RateLimitBackend):
    def __init__(self):
        self.counter = 0

    def consume(self, key, amount, max, bucket_size):
        self.counter += amount
        return self.counter <= max


class RateLimiterTests(unittest.TestCase):
    def setUp(self):
        ratelimit_backend = MockRateLimitBackend()
        self.ratelimiter = ratelimit.RateLimiter(ratelimit_backend, 10, 60)

    def test_consume(self):
        self.ratelimiter.consume('user_12345')

    def test_consume_over_allowance(self):
        with self.assertRaises(ratelimit.RateLimitExceededException):
            self.ratelimiter.consume('user_12345', amount=11)


class RedisRateLimitBackendTest(unittest.TestCase):
    def setUp(self):
        self.amount = 10
        redis = mock.create_autospec(StrictRedis)
        pipeline_context = redis.pipeline.return_value.__enter__.return_value
        pipeline_context.execute.return_value = [self.amount]
        self.ratelimit_backend = RedisRateLimitBackend(redis)

    def test_consume(self):
        self.assertTrue(self.ratelimit_backend.consume(
            'user_12345', self.amount, 10, 60))

    def test_consume_over_max(self):
        self.assertFalse(self.ratelimit_backend.consume(
            'user_12345', self.amount, 5, 60))

class MemcacheRateLimitBackendTest(unittest.TestCase):
    def setUp(self):
        self.amount = 10
        memcache = mock.create_autospec(PooledClient)
        pipeline_context = memcache.incr.return_value = self.amount
        self.ratelimit_backend = MemcacheRateLimitBackend(memcache)

    def test_consume(self):
        self.assertTrue(self.ratelimit_backend.consume(
            'user_12345', self.amount, 10, 60))

    def test_consume_over_max(self):
        self.assertFalse(self.ratelimit_backend.consume(
            'user_12345', self.amount, 5, 60))
