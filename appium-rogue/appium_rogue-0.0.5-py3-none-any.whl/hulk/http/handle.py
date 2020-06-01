# -*- coding: utf-8 -*-

from .error import ParseError, InvalidParamsError, MethodNotFound, InternalError, InvalidRequestError, ServerError

_JSON_RPC_ERR_MAP = {
    -32700: ParseError,
    -32600: InvalidRequestError,
    -32601: MethodNotFound,
    -32602: InvalidParamsError,
    -32603: InternalError,
}


def json_rpc_checker(json):
    error = json.get('error', None)
    if error is None:
        return True

    err_code = error.get('code', 0)
    err_msg = error.get('message', '')

    if err_code in _JSON_RPC_ERR_MAP:
        raise _JSON_RPC_ERR_MAP[err_code](err_msg)

    if -32099 <= err_code <= -32000:
        raise ServerError(err_msg)

    return False
