import copy

__txid_schema = {
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
        }
    },
    'required': [
        'transfer_id',
        'txid'
    ],
    'additionalProperties': False
}


def get_txid_schema() -> dict:
    clone_schema = copy.deepcopy(__txid_schema)
    return clone_schema
