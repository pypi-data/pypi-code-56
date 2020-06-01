import copy

__callback_schema = {
  'type': 'object',
  'properties': {
    'callback_url': {
      'type': 'string',
      'format': 'uri'
    }
  },
  'required': [
    'callback_url'
  ],
  'additionalProperties': False
}


def get_callback_schema() -> dict:
    clone_schema = copy.deepcopy(__callback_schema)
    return clone_schema
