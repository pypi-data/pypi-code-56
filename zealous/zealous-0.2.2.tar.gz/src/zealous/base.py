from __future__ import annotations

import copy

from typing import Any
from typing import Dict
from typing import Generic
from typing import Tuple
from typing import Union

from typing_extensions import Protocol
from typing_extensions import runtime_checkable

from .typing import SchemaInContraT
from .typing import SchemaOutCoT
from .typing import TypeVar


__all__ = (
    "App",
    "Boundary",
    "BoundaryT",
    "Resource",
    "Interface",
    "InterfaceNoBody",
)


@runtime_checkable
class Interface(Protocol[SchemaInContraT, SchemaOutCoT]):
    async def __call__(self, body: SchemaInContraT) -> SchemaOutCoT:
        ...


@runtime_checkable
class InterfaceNoBody(Protocol[SchemaOutCoT]):
    async def __call__(self) -> SchemaOutCoT:
        ...


InterfacesT = Dict[str, Union[Interface[Any, Any], InterfaceNoBody[Any]]]


class ResourceMeta(type):
    def __init__(
        cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]
    ) -> None:
        super().__init__(name, bases, namespace)
        cls.__interfaces__: InterfacesT = {}
        # pylint false positive below: https://github.com/PyCQA/pylint/issues/3268
        cls._collect__interfaces__(namespace)  # pylint: disable=no-value-for-parameter

    def _collect__interfaces__(cls, namespace: Dict[str, Any]) -> None:
        try:
            annotations: Dict[str, Any] = namespace["__annotations__"]
        except KeyError:
            return

        for key, value in annotations.items():
            try:
                is_interface = isinstance(value, Interface)
            except TypeError:
                is_interface = False

            if is_interface:
                cls.__interfaces__[key] = value


class Resource(metaclass=ResourceMeta):
    """App resource specification."""

    def __init__(self) -> None:
        # redeclare _resources since mypy & pylint don't recognize attribute from mcs
        self.__interfaces__: InterfacesT


ResourcesT = Dict[str, Resource]


class BoundaryMeta(type):
    def __init__(
        cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]
    ) -> None:
        super().__init__(name, bases, namespace)
        cls.__resources__: ResourcesT = {}
        # pylint false positive below: https://github.com/PyCQA/pylint/issues/3268
        cls._collect__resources__(namespace)  # pylint: disable=no-value-for-parameter

    def _collect__resources__(cls, namespace: Dict[str, Any]) -> None:
        for key, value in namespace.items():
            try:
                is_subclass = issubclass(value, Resource)
            except TypeError:
                if isinstance(value, Resource):
                    cls.__resources__[key] = value
            else:
                # convert to instance
                if is_subclass:
                    value = value()
                    cls.__resources__[key] = value


class Boundary(metaclass=BoundaryMeta):
    """App boundary."""

    def __init__(self) -> None:
        # redeclare _resources since mypy & pylint don't recognize attribute from mcs
        self.__resources__: ResourcesT

        # A copy of each resource is made in order to avoid inadvertantly modifying the
        # class attribute. For example, a mixin may choose to attach metadata directly
        # on the resource instances.
        for attr in self.__resources__.keys():
            resource = self.__resources__[attr]
            resource_copy = copy.deepcopy(resource)
            setattr(self, attr, resource_copy)
            self.__resources__[attr] = resource_copy


BoundaryT = TypeVar("BoundaryT", bound=Boundary)


class App(Generic[BoundaryT]):
    def __init__(self, boundary: BoundaryT, **_kwargs: Any) -> None:
        self._boundary = boundary
