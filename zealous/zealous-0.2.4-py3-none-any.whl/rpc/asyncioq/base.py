from __future__ import annotations

import asyncio
import uuid

from dataclasses import dataclass
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

from zealous import Schema

from ..base import BaseRPCDriver
from ..base import RPCContext


__all__ = ("AsyncioQRPCDriver",)


class AsyncioQRPCMessageDriverContext:
    def __init__(self) -> None:
        self.uuid = uuid.uuid4().hex


AsyncioQRPCContext = RPCContext[AsyncioQRPCMessageDriverContext]


@dataclass
class MessageIn:
    context: AsyncioQRPCContext
    body: Optional[Schema]


@dataclass
class MessageOut:
    context: AsyncioQRPCContext
    body: Union[Schema, Tuple[Schema, ...], None]


class AsyncioQRPCDriver(BaseRPCDriver[AsyncioQRPCMessageDriverContext]):
    def __init__(self, *, maxsize: int = 0) -> None:
        super().__init__()
        self.maxsize = maxsize

        self.__in_queue: Optional[asyncio.Queue[MessageIn]] = None
        self._out_queues: Dict[str, asyncio.Queue[MessageOut]] = {}

    @property
    def _in_queue(self) -> asyncio.Queue[MessageIn]:
        """Defers creation of asyncio.Queue until used in event loop."""
        if self.__in_queue is None:
            self.__in_queue = asyncio.Queue(maxsize=self.maxsize)
        return self.__in_queue

    def reset(self) -> None:
        self.__in_queue = None
        self._out_queues.clear()

    def make_driver_context(  # pylint: disable=no-self-use
        self,
    ) -> AsyncioQRPCMessageDriverContext:
        return AsyncioQRPCMessageDriverContext()

    async def push_rpc_message_in(
        self, context: AsyncioQRPCContext, body: Optional[Schema]
    ) -> None:
        await self._in_queue.put(MessageIn(context, body))
        self._out_queues[context.driver_context.uuid] = asyncio.Queue(
            maxsize=self.maxsize
        )

    async def pop_rpc_message_in(self,) -> Tuple[AsyncioQRPCContext, Optional[Schema]]:
        message_in = await self._in_queue.get()
        return message_in.context, message_in.body

    async def push_rpc_message_out(
        self,
        context: AsyncioQRPCContext,
        response_body: Union[Schema, Tuple[Schema, ...], None],
    ) -> None:
        await self._out_queues[context.driver_context.uuid].put(
            MessageOut(context, response_body)
        )

    async def pop_rpc_message_out(
        self, context: AsyncioQRPCContext
    ) -> Union[Schema, Tuple[Schema, ...], None]:
        message_out = await self._out_queues[context.driver_context.uuid].get()
        del self._out_queues[context.driver_context.uuid]
        return message_out.body
