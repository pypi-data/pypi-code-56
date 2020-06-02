#! /usr/bin/env python3
#
# Client Example for webrepl and dummy
#
# This file is part of Zepl Broker: https://gitlab.com/zepl1/zepl-broker
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3
import sys, json, zmq, asyncio

SUBSCRIPTIONS = [''] # http://wiki.zeromq.org/whitepapers:message-matching

def main():
    """Command line tool, entry point"""

    import argparse

    parser = argparse.ArgumentParser(
        description='Zepl Client')

    subparsers = parser.add_subparsers(help='commands')
    subparser_log = subparsers.add_parser('log', help='log listener')
    subparser_dev = subparsers.add_parser('dev', help='send to device/runner')
    subparser_ctrl = subparsers.add_parser('ctrl', help='broker ctrl interface')

    subparser_log.add_argument(
        'log',
        help='log commands',
        nargs='?',
        choices=('all', ),
        default='all')

    subparser_dev.add_argument(
        'dev',
        help='dev commands',
        nargs='?',
        choices=('greet', 'sync', 'run'),
        default='greet')

    subparser_dev.add_argument(
        'dev_id',
        help='dev_id of target')

    subparser_dev.add_argument(
        'app',
        nargs='?',
        help='input for mp example app -- single character')

    subparser_ctrl.add_argument(
        'ctrl',
        help='ctrl commands',
        nargs='?',
        choices=('get', 'add'),
        default='get')

    parser.add_argument(
        '--broker',
        nargs='?',
        help='hostname or ip of broker',
        default='localhost')

    parser.add_argument(
        '--config',
        nargs='?',
        help='device config',
        default=False)

    parser.add_argument(
        '-d',
        help='dummy: spawns dummy devices from config',
        action='store_true',
        default=False)

    args = parser.parse_args()

    if args.config:
        with open(args.config, "r") as f:
            cfg = json.load(f)

    ctx = zmq.Context()
    if args.d:
        from zepl_broker import DummyClient
        client = DummyClient(ctx, args.broker)
    else:
        from zepl_broker import WebReplClient
        client = WebReplClient(ctx, args.broker)

    print(f'-- Starting Zepl Client --')
    try:
        if 'log' in args:
            for dev_id in SUBSCRIPTIONS:
                client.log_sub(dev_id)
            while True:
                client.print_log()
        elif 'dev' in args:
            if 'greet' in args.dev:
                client.greet(args.dev_id)
            else:
                if 'sync' in args.dev:
                    client.sync_files(args.dev_id)
                if 'run' in args.dev:
                    client.run_app(args.dev_id, args.app)
        elif 'ctrl' in args:
            if 'get' in args.ctrl:
                client.show_devices()
            elif 'add' in args.ctrl:
                if args.d:
                    ## spawn dummy devices locally
                    from zepl_device.devices.dummy import DummyDevice
                    dctx = zmq.asyncio.Context()
                    for dev_id in cfg.keys():
                        d = DummyDevice(dctx, cfg[dev_id])
                        d.start()
                        client.add_device(dev_id, cfg[dev_id])
                    loop = asyncio.get_event_loop()
                    loop.run_forever()
                else:
                    for dev_id in cfg.keys():
                        client.add_device(dev_id, cfg[dev_id])
    except Exception as e:
        print(e)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
