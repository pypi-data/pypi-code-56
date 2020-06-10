import argparse
import logging
import sys
from logging import basicConfig, CRITICAL, ERROR, WARNING, INFO, DEBUG

from rich.logging import RichHandler


def inspect_apk(args):
    from .inspect.inspecter import do_inspect
    result = do_inspect(args.path)

    if result is None:
        return False

    from .inspect.output import rich_text
    rich_text(result)
    return True


def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    from rich.traceback import install
    install()

    parser = argparse.ArgumentParser("eadb")

    parser.add_argument("-v", "--verbose", action="count")
    parser.add_argument("-q", "--quiet", action="count")

    subparsers = parser.add_subparsers(title='support commands')

    # inspect
    inspect = subparsers.add_parser('inspect', help='inspect apk file, usage: eadb inspect path/to/apk')
    inspect.add_argument('path', metavar='APK_PATH', help='the apk path')

    inspect.set_defaults(func=inspect_apk)

    # analyze catcher
    analyze_catcher = subparsers.add_parser('analyze_cather')

    # foo
    foo = subparsers.add_parser('foo')

    args = parser.parse_args(argv)

    log_level = WARNING

    if args.verbose:
        log_level = DEBUG

    if args.quiet:
        log_level = CRITICAL

    FORMAT = "%(message)s"
    basicConfig(level=log_level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
