"""The test_base module contains unit tests for the pyaid.base module."""

# ---------------- TESTS ----------------
import unittest
from unittest.mock import MagicMock, sentinel

from pyaid.base import *


class TestClassProperty(unittest.TestCase):
    def test_get_set(self):
        get_only_cls = MagicMock()
        get_set_get_cls = MagicMock()
        get_set_set_cls = MagicMock()

        class Z(object, metaclass=classproperty.meta):
            _get_set = sentinel.nothing

            @classproperty
            def get_only(cls): # noqa
                get_only_cls(cls)
                return sentinel.get_only

            @classproperty
            def get_set(cls): # noqa
                get_set_get_cls(cls)
                return cls._get_set

            @get_set.setter
            def get_set(cls, value): # noqa
                get_set_set_cls(cls)
                cls._get_set = value

        for c, msg in [(Z, "class"), (Z(), "instance")]:
            with self.subTest(msg=msg):
                # Reset
                Z._get_set = sentinel.nothing

                # Test get_only
                self.assertEqual(sentinel.get_only, c.get_only)
                get_only_cls.assert_called_once_with(Z)
                get_only_cls.reset_mock()

                # Should return our initial "nothing" value
                self.assertEqual(sentinel.nothing, c.get_set)
                get_set_get_cls.assert_called_once_with(Z)
                get_set_get_cls.reset_mock()

                # Now test the set
                c.get_set = sentinel.get_set_val
                get_set_set_cls.assert_called_once_with(Z)
                get_set_set_cls.reset_mock()

                self.assertEqual(sentinel.get_set_val, c.get_set)
                get_set_get_cls.assert_called_once_with(Z)
                get_set_get_cls.reset_mock()

    def test_read_only(self):
        class Z(object, metaclass=classproperty.meta):
            _get_set = sentinel.nothing

            @classproperty
            def get_only(cls): # noqa
                return sentinel.get_only

        self.assertEqual(sentinel.get_only, Z.get_only)
        with self.assertRaises(AttributeError):
            Z.get_only = 123

    def test_proper_metaclass(self):
        class Z(object):
            _get_set = sentinel.nothing

            @classproperty
            def get_only(cls): # noqa
                return sentinel.get_only

        with self.assertRaises(TypeError):
            self.assertEqual("should not resolve", Z.get_only)


if __name__ == "__main__":
    unittest.main()
