import copy

__post_txid_schema = {
    'type': 'object',
    'properties': {
        'transfer_id': {
            'type': 'string',
            'minLength': 64,
            'maxLength': 64
        },
        'txid': {
            'type': 'string',
            'minLength': 1
        },
        'signature': {
            'type': 'string',
            'minLength': 128,
            'maxLength': 128,
            'pattern': '^[0123456789A-Fa-f]+$'
        }
    },
    'required': [
        'transfer_id',
        'txid',
        'signature'
    ],
    'additionalProperties': False
}


def get_post_txid_schema() -> dict:
    clone_schema = copy.deepcopy(__post_txid_schema)
    return clone_schema
