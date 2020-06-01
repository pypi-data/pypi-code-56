import copy

__beneficiary_endpoint_url_schema = {
    "type": "object",
    "properties": {
        "vasp_code": {
            "type": "string",
            "minLength": 1
        },
        "callback_permission_request_url": {
            "type": "string",
            "format": "uri"
        },
        "callback_txid_url": {
            "type": "string",
            "format": "uri"
        }
    },
    "anyOf": [
        {
            "required": ["vasp_code", "callback_permission_request_url"]
        },
        {
            "required": ["vasp_code", "callback_txid_url"]
        }
    ],
    "additionalProperties": False
}


def get_beneficiary_endpoint_url_schema() -> dict:
    clone_schema = copy.deepcopy(__beneficiary_endpoint_url_schema)
    return clone_schema
