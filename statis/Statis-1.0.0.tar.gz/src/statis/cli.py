"""
Command line argument parsing and logging configuration.

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
import logging
import sys
from typing import List

from statis import notification
from statis._version import __version__


def parse_args(arg_list: List[str]) -> argparse.Namespace:
    """
    Parse and return any provided command line arguments.

    :return: A namespace holding all parsed arguments
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] [module [notifier] [notifier_args...]]',
        description='Modular system monitoring and status display via '
                    'desktop notifications.',
        epilog='examples:\n'
               '  %(prog)s cpu usage --core 2\n'
               '  %(prog)s memory free\n'
               '  %(prog)s time',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('module', nargs='?',
                        help='the module (e.g. \033[3mcpu\033[0m) of which '
                             'to run a notifier')
    parser.add_argument('notifier', nargs='?', default='',
                        help='the notifier to run (equal to <\033[1mmodule'
                             '\033[0m> if empty)')
    parser.add_argument('notifier_args', nargs=argparse.REMAINDER,
                        help='further arguments passed to the given notifier')

    parser.add_argument('-V', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list all available notifiers grouped by module')

    parser.add_argument('-t', '--timeout', type=float, metavar='N', default=4,
                        help='time in seconds until the notification expires\n'
                             '(default: %(default).1f)')
    parser.add_argument('-u', '--urgency', metavar='LEVEL',
                        default=notification.Urgency.LOW.value,
                        choices=[u.value for u in notification.Urgency],
                        help='an urgency LEVEL to send the notification with\n'
                             'one of: {%(choices)s} (default: %(default)s)')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="print additional messages on what's being done")
    parser.add_argument('-d', '--debug', action='store_true',
                        help='print detailed logs to aid in debugging')

    args: argparse.Namespace = parser.parse_args(arg_list)

    if not args.list and args.module is None:
        parser.print_help()
        sys.exit(2)

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    return args


def setup_logging() -> None:
    """
    Configure the logging format to include colored [level] prefixes.
    """
    logging.basicConfig(format='[%(levelname)s\033[0m] %(message)s')

    logging.addLevelName(logging.DEBUG, '\033[1;35mD')
    logging.addLevelName(logging.INFO, '\033[1;34mI')
    logging.addLevelName(logging.WARNING, '\033[1;33mW')
    logging.addLevelName(logging.ERROR, '\033[1;31mE')
    logging.addLevelName(logging.CRITICAL, '\033[1;31mC')
