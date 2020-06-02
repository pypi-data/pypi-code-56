import unittest
import typing
import argparse

from sett.cli import cli_builder


def cli_args(args):
    def dec(fn):
        fn.test_args = args
        return fn
    return dec


@cli_args(["-x", "1", "--longname"])
def f(x: int, longname: bool):
    assert x == 1 and longname


@cli_args(["1"])
def g(x: int, *, longname: bool):
    assert x == 1 and not longname


@cli_args(["--longname", "1", "2"])
def h(x: typing.List[int], *, longname: bool = False):
    assert x == [1, 2] and longname


class TestAddArgumentsBySignature(unittest.TestCase):
    def setUp(self):
        self.functions = (f, g, h)

    def test_arguments_by_signature(self):
        for fn in self.functions:
            with self.subTest(f=fn.__name__):
                parser = argparse.ArgumentParser()
                args = cli_builder.arguments_by_signature(fn)
                for arg in args:
                    parser.add_argument(*arg.args, **arg.kwargs)
                cmd_args = parser.parse_args(fn.test_args)
                fn(**vars(cmd_args))

    def test_arguments_by_signature_optional(self):
        def opt_f(s: typing.Optional[str]):
            assert s == "s"
        with self.assertRaises(ValueError):
            args = list(cli_builder.arguments_by_signature(opt_f))

        args = cli_builder.arguments_by_signature(
            opt_f, overrides={"s": dict(default="s")})
        parser = argparse.ArgumentParser()
        for arg in args:
            parser.add_argument(*arg.args, **arg.kwargs)
            cmd_args = parser.parse_args([])
        opt_f(**vars(cmd_args))
        cmd_args = parser.parse_args(["-s", "s"])
        opt_f(**vars(cmd_args))

    def test_invalid_override(self):
        with self.assertRaises(ValueError):
            list(cli_builder.arguments_by_signature(
                f, overrides={"y": {}}))


class TestSubcommands(unittest.TestCase):
    def setUp(self):
        self.functions = (f, g, h)

    def test_subcommands(self):
        class Cli(cli_builder.Subcommands):
            subcommands = [cli_builder.Subcommand(fn)
                           for fn in self.functions]

        for fn in self.functions:
            with self.subTest(f=fn.__name__):
                Cli([fn.__name__] + fn.test_args)


class TestUtils(unittest.TestCase):
    def _decorator_routine_check(self, fct, decorator):
        self.assertEqual(decorator(fct).__name__, fct.__name__)
        self.assertEqual(decorator(fct).__doc__, fct.__doc__)

    def test_lazy_partial(self):
        def _f(x, y, z=-1, w=-2):
            return x, y, z, w
        self._decorator_routine_check(_f, cli_builder.lazy_partial())
        _g = cli_builder.lazy_partial(lambda: 1, w=lambda: 4)(_f)
        self.assertEqual(_g(2, 3), (1, 2, 3, 4))
        self.assertEqual(_g(y=2, z=3, w=5), (1, 2, 3, 5))

    def test_lazy_partial_preserves_keywords(self):
        def _f(x, y, z=-1, w=-2):
            return x, y, z, w
        _f.keywords = {"z": -1}

        def cb():
            return 1
        _g = cli_builder.lazy_partial(cb)(_f)
        self.assertEqual(_g.keywords, _f.keywords)
        self.assertEqual(_g.args, (cb,))

    def test_partial(self):
        def _f(x, y, z=-1, w=-2):
            return x, y, z, w
        self._decorator_routine_check(_f, cli_builder.partial())
        _g = cli_builder.partial(1, w=4)(_f)
        self.assertEqual(_g(2, 3), (1, 2, 3, 4))
        self.assertEqual(_g(y=2, z=3, w=5), (1, 2, 3, 5))

    def test_rename(self):
        def _f():
            return 1
        _g = cli_builder.rename("g")(_f)
        self.assertEqual(_g.__name__, "g")
        self.assertEqual(_f.__doc__, _g.__doc__)
        self.assertEqual(_f(), _g())

    def test_set_default(self):
        def _f(x, y, z=-1, w=-2):
            return x, y, z, w
        self._decorator_routine_check(_f, cli_builder.set_default())
        _g = cli_builder.set_default(w=4)(_f)
        self.assertEqual(_g(2, 3), (2, 3, -1, 4))
        self.assertEqual(_g(x=1, y=2, z=3, w=5), (1, 2, 3, 5))
