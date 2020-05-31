# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict, List

import attr


@attr.s
class OperationLogServiceException(Exception):
    code: int = attr.ib(default=230000)
    msg: str = attr.ib(default="")


@attr.s
class OperationLog:
    time: datetime = attr.ib(default=datetime.now())
    topic: str = attr.ib(default="")
    source: str = attr.ib(default="")
    tags: Dict[str, str] = attr.ib(default={})
    content: str = attr.ib(default="")


@attr.s
class OperationLogPageList:
    logs: List[OperationLog] = attr.ib(default=[])
    total: int = attr.ib(default=0)
