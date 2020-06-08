import decimal
import logging
import typing

from ern_reactor import ErcoinReactor

from mailflagger.client import Client as MFClient


logger = logging.getLogger(__name__)


def modify_subparser(subparser):
    group = subparser.add_argument_group('Ercoin')
    group_enable = group.add_mutually_exclusive_group()
    group_enable.add_argument(
        '--ercoin-enable',
        action='store_true',
        help='Enable Ercoin',
    )
    group_enable.add_argument(
        '--ercoin-no-enable',
        dest='ercoin_enable',
        action='store_false',
        help='Disable Ercoin',
    )
    group.add_argument(
        '--ercoin-address',
        help='Base64-encoded address',
    )
    group.add_argument(
        '--ercoin-node',
    )
    group.add_argument(
        '--ercoin-port',
        type=int,
        default=443,
    )
    group_ssl = group.add_mutually_exclusive_group()
    group_ssl.add_argument(
        '--ercoin-ssl',
        action='store_true',
        help='Enable SSL',
    )
    group_ssl.add_argument(
        '--ercoin-no-ssl',
        dest='ercoin_ssl',
        action='store_false',
        help='Disable SSL',
    )
    group.add_argument(
        '--ercoin-threshold',
        help='Threshold in ercoins, with dot as decimal separator',
    )


def _msg_to_str(msg: bytes) -> typing.Optional[str]:
    try:
        return msg.decode('utf-8')
    except UnicodeDecodeError:
        return None


class FlaggerReactor(ErcoinReactor):
    def __init__(self, **kwargs):
        args = kwargs.pop('args')
        self._threshold: int = kwargs.pop('threshold')
        self._mf_client = MFClient(args, asynchronous=True)
        super().__init__(**kwargs)

    def get_namespace(self):
        return 'mailflagger'

    async def process_tx(self, tx):
        if tx['value'] >= self._threshold and (message_str := _msg_to_str(tx['message'])):
            logger.debug(f'Transaction {tx["hash"]} is eligible.')
            await self._mf_client.send({'query': message_str})
            reply = await self._mf_client.recv()
            assert reply.get('processed')
        else:
            logger.debug(f'Skipping transaction {tx["hash"]} (not eligible)…')


async def foo(args):
    import asyncio
    with MFClient(args, asynchronous=True) as client:
        while True:
            await client.send({'query': 'foo'})
            await asyncio.sleep(1)
            await client.recv()


def daemon_coroutine(args):
    reactor = FlaggerReactor(
        node=args.ercoin_node,
        address=args.ercoin_address,
        ssl=args.ercoin_ssl,
        threshold=int(decimal.Decimal(args.ercoin_threshold) * 10**6),
        port=args.ercoin_port,
        args=args,
    )
    return reactor.start()


def daemon_coroutines(args):
    if args.ercoin_enable:
        yield daemon_coroutine(args)
