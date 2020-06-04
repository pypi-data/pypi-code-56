"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
import logging
import sys
from typing import Dict, List

from statis import cli, search
from statis import notification as nf
from statis.notifier import NotifierError


def main(arg_list: List[str] = None) -> int:
    """
    Initialize, parse CLI arguments, and run a specified notifier.

    :return: An exit status to terminate the process with
    """
    if arg_list is None:
        arg_list = sys.argv[1:]

    cli.setup_logging()

    args: argparse.Namespace = cli.parse_args(arg_list)
    if args.list:
        _print_notifier_list()
        return 0

    try:
        notifier = search.find_notifier(args.module, args.notifier)
    except FileNotFoundError as e:
        logging.error(str(e))
        return 1

    notifier.parse_args(args.notifier_args)

    replace_id: int = nf.id_from_string(args.module + args.notifier)

    try:
        notification: nf.Notification = notifier.run()
        nf.send(notification, args.timeout, args.urgency, replace_id)
    except NotifierError as e:
        logging.error('Failed to run notifier: %s', e)
        return 1

    return 0


def _print_notifier_list() -> None:
    """
    Print a list of all available notifiers grouped by module.
    """
    notifiers_by_module: Dict[str, List[str]] = search.list_all()
    for module in notifiers_by_module:
        print(module)
        for notifier in notifiers_by_module[module]:
            print(f' * {notifier}')


if __name__ == '__main__':
    sys.exit(main())
