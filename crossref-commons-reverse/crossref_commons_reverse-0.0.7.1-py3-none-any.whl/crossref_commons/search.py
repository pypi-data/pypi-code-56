import json

from crossref_commons.config import API_URL, DATA_URL
from crossref_commons.http_utils import remote_call, uencplus


def search_publication(query, sort=None, order=None):
    if not isinstance(query, str):
        fields = [
            "query.{}={}".format(uencplus(key), uencplus(value))
            for (key, value) in query
        ]
        query_str = "&".join(fields)
    else:
        query_str = "query={}".format(uencplus(query))

    sort_str = ""
    if sort:
        sort_str = "&sort={}".format(uencplus(sort))

    order_str = ""
    if order:
        order_str = "&order={}".format(uencplus(order))

    parameter_str = query_str + sort_str + order_str

    code, result = remote_call(API_URL, 'works?{}'.format(parameter_str))
    if code != 200:
        raise ConnectionError('API returned code {}'.format(code))

    result_data = json.loads(result)

    if result_data['status'] != 'ok':
        raise ValueError("API returned non-successful status '{}'".format(
            result_data['status']))
    if result_data['message-type'] != 'work-list':
        raise ValueError("Expected a 'work-list', got a '{}'".format(
            result_data['message-type']))

    count = int(result_data['message']['total-results'])
    results = result_data['message']['items']

    return (count, results)
