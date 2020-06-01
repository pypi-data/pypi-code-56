from __future__ import annotations

import abc
import asyncio
import logging

from dataclasses import dataclass
from typing import Any
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from typing import cast
from typing import overload

from zealous import ErrorSchema
from zealous import Schema
from zealous.base import App
from zealous.base import Boundary
from zealous.base import BoundaryT
from zealous.base import Interface
from zealous.base import InterfaceNoBody
from zealous.base import Resource
from zealous.typing import SchemaInContraT
from zealous.typing import SchemaOutCoT

from . import exceptions


__all__ = (
    "RPCClientAppMixin",
    "RPCClientConf",
    "RPCServerAppMixin",
    "RPCServerConf",
)

LOG = logging.getLogger(__name__)


DriverContextT = TypeVar("DriverContextT")


class RPCContext(Generic[DriverContextT]):
    def __init__(
        self, *, resource: str, interface: str, driver_context: DriverContextT,
    ) -> None:
        self.resource = resource
        self.interface = interface
        self.driver_context = driver_context


class BaseRPCDriver(Generic[DriverContextT], metaclass=abc.ABCMeta):
    def make_context(
        self, resource: str, interface: str,
    ) -> RPCContext[DriverContextT]:
        return RPCContext(
            resource=resource,
            interface=interface,
            driver_context=self.make_driver_context(),
        )

    @abc.abstractmethod
    def make_driver_context(self) -> DriverContextT:
        """Hook for attaching driver_context to RPCMessageContext."""

    @abc.abstractmethod
    async def push_rpc_message_in(
        self, context: RPCContext[DriverContextT], body: Optional[Schema]
    ) -> None:
        ...

    @abc.abstractmethod
    async def pop_rpc_message_in(
        self,
    ) -> Tuple[RPCContext[DriverContextT], Optional[Schema]]:
        ...

    @abc.abstractmethod
    async def push_rpc_message_out(
        self,
        context: RPCContext[DriverContextT],
        response_body: Union[Schema, Tuple[Schema, ...], None],
    ) -> None:
        ...

    @abc.abstractmethod
    async def pop_rpc_message_out(
        self, context: RPCContext[DriverContextT]
    ) -> Union[Schema, Tuple[Schema, ...], None]:
        ...


@dataclass
class RPCClientConf:
    driver: BaseRPCDriver[Any]


class RPCClient:
    def __init__(self, conf: RPCClientConf, boundary: Boundary) -> None:
        """Hook up RPCResourceClient as per the boundary's specification."""
        for attr, resource in boundary.__resources__.items():
            setattr(self, attr, RPCResourceClient(conf, resource, attr))


class RPCResourceClient:
    """RPC client for a specific resource."""

    def __init__(
        self, conf: RPCClientConf, resource: Resource, resource_name: str
    ) -> None:
        """Hook up RPCInterfaceClient as per resource definition."""
        for attr, interface in resource.__interfaces__.items():
            setattr(
                self, attr, RPCInterfaceClient(conf, interface, resource_name, attr),
            )


class RPCInterfaceClient(Interface[SchemaInContraT, SchemaOutCoT]):
    """RPC client for a specific resource interface."""

    def __init__(
        self,
        conf: RPCClientConf,
        interface: Union[Interface[Any, Any], InterfaceNoBody[Any]],
        resource_name: str,
        interface_name: str,
    ):
        self._conf = conf
        self._interface = interface
        self._resource_name = resource_name
        self._interface_name = interface_name

    async def __call__(self, body: SchemaInContraT = None) -> SchemaOutCoT:
        context = self._conf.driver.make_context(
            self._resource_name, self._interface_name
        )
        await self._conf.driver.push_rpc_message_in(context, body)
        response_body = await self._conf.driver.pop_rpc_message_out(context)
        if isinstance(response_body, ErrorSchema):
            raise exceptions.RPCRemoteError(
                exc_type=response_body.type, exc_message=response_body.message
            )
        # if the response_body is not an error, the type is enforced by the interface
        return cast(SchemaOutCoT, response_body)


class RPCClientAppMixin(App[BoundaryT]):
    """Provides RPC Client implementation for Boundary."""

    def __init__(self, boundary: BoundaryT) -> None:
        super().__init__(boundary)
        self._rpc_client: Optional[RPCClient] = None

    @property
    @abc.abstractmethod
    def __rpc_client__(self) -> RPCClientConf:
        ...

    @property
    def rpc_client(self) -> BoundaryT:
        if self._rpc_client is None:
            self._rpc_client = RPCClient(self.__rpc_client__, self._boundary)
        # for all intents and purposes, this is just an implementation of the boundary
        return cast(BoundaryT, self._rpc_client)


@dataclass
class RPCServerConf:
    driver: BaseRPCDriver[Any]
    impl: Boundary
    n_workers: int = 1


class RPCServerAppMixin(App[BoundaryT]):
    """Provides RPC server implementation for Boundary."""

    def __init__(self, boundary: BoundaryT) -> None:
        super().__init__(boundary)
        self._rpc_server: Optional[RPCServer] = None

    @property
    @abc.abstractmethod
    def __rpc_server__(self) -> RPCServerConf:
        ...

    @property
    def rpc_server(self) -> RPCServer:
        if self._rpc_server is None:
            self._rpc_server = RPCServer(self.__rpc_server__)
        return self._rpc_server


HandlerReturns = Union[Schema, Tuple[Schema, ...], None]


class RPCServer:
    def __init__(self, conf: RPCServerConf) -> None:
        self._conf = conf

        if self._conf.n_workers < 1:
            raise exceptions.RPCServerInvalidConfig(
                reason="RPCServer n_workers must be >= 1"
            )
        self._worker_tasks: Optional[List[asyncio.Task[None]]] = None

    async def start(self) -> None:
        if self._worker_tasks:
            raise exceptions.RPCServerAlreadyStarted
        self._worker_tasks = [
            asyncio.create_task(self.loop()) for _ in range(self._conf.n_workers)
        ]

    async def stop(self) -> None:
        if not self._worker_tasks:
            raise exceptions.RPCServerNotStarted
        for task in self._worker_tasks:
            task.cancel()
        await asyncio.gather(*self._worker_tasks)
        self._worker_tasks = None

    async def loop(self) -> None:
        while True:
            try:
                await self.loop_once()
            except asyncio.CancelledError:
                LOG.debug("Server loop cancelled. Leaving.")
                break
            except Exception:  # pylint: disable=broad-except
                LOG.exception("Error caught in server loop. Continuing...")

    async def loop_once(self) -> None:
        context, body = await self._conf.driver.pop_rpc_message_in()
        try:
            response_body = await self.delegate_rpc_message(context, body)
        except Exception:  # pylint: disable=broad-except
            logging.exception("Exception caught during message delegation.")
            response_body = ErrorSchema.from_exc_info()
        await self._conf.driver.push_rpc_message_out(context, response_body)

    async def delegate_rpc_message(
        self, context: RPCContext[Any], body: Optional[Schema]
    ) -> Union[Schema, Tuple[Schema, ...], None]:
        """Delegate RPC message received server-side."""

        handler_fn, args = self.get_handler_fn(context, body)
        return await handler_fn(*args)

    @overload
    def get_handler_fn(
        self, context: RPCContext[Any], body: None
    ) -> Tuple[InterfaceNoBody[HandlerReturns], Tuple[()]]:
        ...

    @overload
    def get_handler_fn(
        self, context: RPCContext[Any], body: Schema
    ) -> Tuple[Interface[Schema, HandlerReturns], Tuple[Schema]]:
        ...

    def get_handler_fn(
        self, context: RPCContext[Any], body: Optional[Schema]
    ) -> Union[
        Tuple[Interface[Schema, HandlerReturns], Tuple[Schema]],
        Tuple[InterfaceNoBody[HandlerReturns], Tuple[()]],
    ]:
        resource: Resource = getattr(self._conf.impl, context.resource)
        try:
            if body:
                return getattr(resource, context.interface), (body,)
            return getattr(resource, context.interface), ()
        except AttributeError:
            raise exceptions.RPCServerInterfaceNotImplemented(
                resource=context.resource, interface=context.interface
            )
