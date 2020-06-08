import decimal
import re
import typing

import mt940

from mailflagger.client import Client


def modify_subparser(subparser):
    subparser.add_argument(
        'file',
        widget='FileChooser',
    )
    subparser.add_argument(
        '--banking-threshold',
        required=True,
    )
    subparser.add_argument(
        '--banking-title-prefix',
        help='Title prefix which will be used to filter relevant transfers',
        type=str,
        default='',
    )


def _tx_to_title(tx):
    return re.search(r'<20"([^"]*)"', tx.data['transaction_details']).group(1)


def _tx_to_amount(tx):
    return tx.data['amount'].amount


def _extract_query(tx, args) -> typing.Optional[str]:
    if match := re.match(
            f'{args.banking_title_prefix}(.*)',
            _tx_to_title(tx),
    ):
        return match.group(1).strip()


def _submit_query(client, query):
    client.send({'query': query})
    reply = client.recv()
    assert reply.get('processed')


def run(args):
    txs = mt940.parse(args.file)
    threshold = decimal.Decimal(args.banking_threshold)
    with Client(args) as c:
        for tx in txs:
            if _tx_to_amount(tx) >= threshold:
                if query := _extract_query(tx, args):
                    _submit_query(c, query)


def command_help(default_args):
    return 'Import banking transfers from a MT940 file.'
