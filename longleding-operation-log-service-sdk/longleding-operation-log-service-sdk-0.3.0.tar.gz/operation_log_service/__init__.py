# -*- coding: utf-8 -*-
import inspect
from datetime import datetime
from typing import Dict, List

from .grpc_client import OperationLogServiceGRPCClient
from .model import OperationLog, OperationLogPageList, OperationLogServiceException
from .schema import OperationLogObjectSchema as LOSch

__all__ = [
    "init_service",
    "log",
    "get_operation_logs",
    "OperationLogServiceException",
    "OperationLog",
    "OperationLogPageList",
]

_client: OperationLogServiceGRPCClient


def param_check(func):
    def wrapper(*args, **kwargs):
        global _client
        assert _client is not None, "operation log service sdk must be init first"
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        for i, v in enumerate(args):
            p = params[i]
            assert p.annotation is inspect.Parameter.empty or isinstance(v, p.annotation), "{} must be {}.".format(p.name, str(p.annotation))
        return func(*args, **kwargs)

    return wrapper


def init_service(endpoint: str, src: str) -> None:
    global _client
    assert type(endpoint) == str, "endpoint must be a str"
    assert type(src) == str, "src must be a str"
    _client = OperationLogServiceGRPCClient(endpoint=endpoint, src=src)


@param_check
def log(time: datetime = datetime.now(),
        topic: str = "",
        tags: Dict[str, str] = None,
        content: str = "") -> None:
    return _client.log(**locals())


@param_check
def get_operation_logs(start_time: datetime,
                       end_time: datetime,
                       offset: int = 0,
                       limit: int = 0,
                       reverse: bool = False,
                       topic_in: List[str] = None,
                       source_in: List[str] = None,
                       tag_contains: Dict[str, List[str]] = None) -> OperationLogPageList:
    return _client.get_logs(**locals())
