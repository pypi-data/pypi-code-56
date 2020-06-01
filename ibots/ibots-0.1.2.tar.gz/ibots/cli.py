import requests
import argparse


def call(server, port, command, kwargs):
    requests.post(
        '{}:{}/{}'.format(server, port, command),
        data=kwargs,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--server',
        help='Server',
        default='http://localhost',
    )
    parser.add_argument(
        '-p',
        '--port',
        help='Port number',
        type=int,
        default=8000,
    )
    subparsers = parser.add_subparsers(dest='command')

    parser_status = subparsers.add_parser('status')
    parser_status.add_argument(
        '-b',
        '--bots',
        nargs='+',
        default=[],
        help='List of bots',
    )

    parser_pause = subparsers.add_parser('pause')
    parser_pause.add_argument(
        '-b',
        '--bots',
        nargs='+',
        default=[],
        help='List of bots',
    )

    parser_resume = subparsers.add_parser('resume')
    parser_resume.add_argument(
        '-b',
        '--bots',
        nargs='+',
        default=[],
        help='List of bots',
    )

    parser_reset = subparsers.add_parser('reset')
    parser_reset.add_argument(
        '-b',
        '--bots',
        nargs='+',
        default=[],
        help='List of bots',
    )

    parser_resource = subparsers.add_parser('resource')
    parser_resource.add_argument(
        'targets',
        nargs='+',
        help='List of resources',
    )
    parser_resource.add_argument(
        'instruction',
        help='Instructions for execution',
    )

    parser_bot = subparsers.add_parser('bot')
    parser_bot.add_argument(
        'targets',
        nargs='+',
        help='List of bots',
    )
    parser_resource.add_argument(
        'instruction',
        help='Instructions for execution',
    )

    parser_bot = subparsers.add_parser('interact')
    parser_bot.add_argument(
        'target',
        help='Bot to interact with',
    )

    kwargs = vars(parser.parse_args())
    call(
        kwargs.pop('server'),
        kwargs.pop('port'),
        kwargs.pop('command'),
        kwargs,
    )
