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


class TestStaticInit(unittest.TestCase):
    def test_static_init(self):
        @static_init
        class Foo:
            bar = 0

            @classmethod
            def static_init(cls):
                cls.bar = 1
        
        self.assertIsNotNone(getattr(Foo, 'bar', None))
        self.assertEqual(Foo.bar, 1)
        Foo.bar = 2
        self.assertEqual(Foo.bar, 2)
        foo = Foo()
        self.assertEqual(Foo.bar, 2)
        Foo.bar = 3
        self.assertEqual(Foo.bar, 3)

    def test_missing_static_init(self):
        @static_init
        class Foo:
            pass

        foo = Foo()

    def test_singleton(self):
        @singleton
        class Foo:
            def __init__(self):
                self.x = 0

        self.assertIsNone(Foo.instance)
        foo = Foo()
        self.assertIsNotNone(Foo.instance)
        self.assertIs(foo, Foo.instance)
        bar = Foo()
        self.assertIsNotNone(Foo.instance)
        self.assertIs(foo, bar)
        self.assertIs(bar, Foo.instance)
        self.assertIs(foo, Foo.instance)
        self.assertEqual(Foo.instance.x, 0)
        self.assertEqual(foo.x, 0)
        self.assertEqual(bar.x, 0)
        Foo.instance.x += 1
        self.assertEqual(Foo.instance.x, 1)
        self.assertEqual(foo.x, 1)
        self.assertEqual(bar.x, 1)
        foo.x += 1
        self.assertEqual(Foo.instance.x, 2)
        self.assertEqual(foo.x, 2)
        self.assertEqual(bar.x, 2)
        bar.x += 1
        self.assertEqual(Foo.instance.x, 3)
        self.assertEqual(foo.x, 3)
        self.assertEqual(bar.x, 3)


if __name__ == "__main__":
    unittest.main()
