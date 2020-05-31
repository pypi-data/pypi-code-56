# -*- coding: utf-8 -*-
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import grpc
from google.protobuf.any_pb2 import Any as pbAny

from . import common_pb2 as c_pb
from . import operationLogService_pb2 as o_pb
from . import operationLogService_pb2_grpc as o_grpc
from .model import OperationLogPageList, OperationLogServiceException
from .schema import GetOperationLogsRequestPbSchema as LRPSch
from .schema import OperationLogPageListObjectSchema as LLOSch
from .schema import OperationLogPageListPbSchema as LLPSch
from .schema import OperationLogPbSchema as LPSch


class OperationLogServiceGRPCClient:

    def __init__(self, endpoint: str, src: str):
        self._endpoint = endpoint
        self._src = src

    @contextmanager
    def _stub(self):
        with grpc.insecure_channel(self._endpoint) as channel:
            stub = o_grpc.OpLogStub(channel)
            try:
                yield stub
            except grpc.RpcError as e:
                raise OperationLogServiceException(msg=str(e))

    def _pack(self, request: Any) -> c_pb.RequestMessage:
        data = pbAny()
        data.Pack(request)
        return c_pb.RequestMessage(src=self._src, data=data)

    def _unpack(self, response: c_pb.ResponseMessage, data_type: Optional[type]) -> Any:
        if response.code != 0:
            raise OperationLogServiceException(code=response.code, msg=response.msg)
        if data_type is None:
            return None
        msg = data_type()
        response.data.Unpack(msg)
        # msg.ParseFromString(response.data.value)
        return msg

    def log(self, time: datetime = datetime.now(),
            topic: str = "",
            tags: Dict[str, str] = None,
            content: str = "") -> None:
        time = time.isoformat()
        tags = tags if tags else {}
        log_message = LPSch().load(locals())
        log_message.source = self._src
        with self._stub() as stub:
            response = stub.Log(self._pack(log_message))
            self._unpack(response, None)

    def get_logs(self,
                 start_time: datetime,
                 end_time: datetime,
                 offset: int = 0,
                 limit: int = 0,
                 reverse: bool = False,
                 topic_in: list = None,
                 source_in: list = None,
                 tag_contains: Dict[str, List[str]] = None) -> OperationLogPageList:
        start_time = start_time.isoformat()
        end_time = end_time.isoformat()
        topic_in = topic_in if topic_in else []
        source_in = source_in if source_in else []
        tag_contains = tag_contains if tag_contains else {}
        req_message = LRPSch().load(locals())
        with self._stub() as stub:
            response = stub.GetOperationLogs(self._pack(req_message))
            llp = self._unpack(response, o_pb.GetOperationLogsResponse)
            llo = LLOSch().load(LLPSch().dump(llp))
            return llo
