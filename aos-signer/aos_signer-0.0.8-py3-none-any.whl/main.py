#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import argparse

from aos_signer.signer.signer import Signer

_COMMAND_INIT = 'init'
_COMMAND_SIGN = 'sign'
_COMMAND_UPLOAD = 'upload'


def run_init_signer():
    pass


def run_sign():
    s = Signer(src_folder='src', package_folder='.')
    s.process()


def main():
    s = Signer(src_folder='src', package_folder='.')
    s.process()
    # p = service_config_parser.ServiceConfigParser('conf.yaml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process service config.')
    parser.set_defaults(which=None)

    sub_parser = parser.add_subparsers(title='Commands')

    init = sub_parser.add_parser(
        _COMMAND_INIT,
        help='Generate Service stub'
    )
    init.set_defaults(which=_COMMAND_INIT)

    sign = sub_parser.add_parser(
        _COMMAND_SIGN,
        help='Sign Service'
    )
    sign.set_defaults(which=_COMMAND_SIGN)

    args = parser.parse_args()
    if args.which is None:
        run_sign()

    if args.which == _COMMAND_INIT:
        run_init_signer()

    if args.which == _COMMAND_SIGN:
        run_sign()
