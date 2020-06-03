from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from functools import lru_cache
from functools import reduce
from functools import wraps
from operator import or_
from typing import Any
from typing import Dict
from typing import Generic
from typing import Hashable
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from pyworkflows.errors import UnhashableParameterError


T = TypeVar("T")


class TaskMeta(ABCMeta):
    def __new__(
        mcs: Type[TaskMeta],
        name: str,
        bases: Union[Type, Tuple[Type, ...]],
        namespace: Dict[str, Any],
    ) -> TaskMeta:
        init_str = "__init__"
        try:
            init = namespace[init_str]
        except KeyError:
            pass
        else:

            @wraps(init)
            def __init__(self: Task, *args: Any, **kwargs: Any) -> None:
                try:
                    self._dependencies_and_parameters
                except AttributeError:
                    pre_attrs = set(dir(self))
                    init(self, *args, **kwargs)
                    new_attrs: Dict[str, Any] = {
                        attr: getattr(self, attr)
                        for attr in set(dir(self)) - pre_attrs
                        if attr != "_dependencies_and_parameters"
                    }
                    dependencies: Set[Task] = {
                        x for x in new_attrs.values() if isinstance(x, Task)
                    }
                    parameters: Dict[str, Hashable] = {
                        k: self._check_hashable(k, v)
                        for k, v in new_attrs.items()
                        if not isinstance(v, Task)
                    }
                    self._dependencies_and_parameters = (
                        dependencies,
                        parameters,
                    )
                else:
                    init(self, *args, **kwargs)
                for key, value in self.get_parameters().items():
                    self._check_hashable(key, value)

            namespace[init_str] = __init__
        return super().__new__(mcs, name, bases, namespace)  # type: ignore


class Task(Generic[T], metaclass=TaskMeta):
    _dependencies_and_parameters: Tuple[Set[Task], Dict[str, Hashable]]

    @abstractmethod
    def __call__(self: Task[T]) -> T:
        raise NotImplementedError

    def __eq__(self: Task[T], other: Any) -> bool:
        if isinstance(other, Task):
            return (
                type(self) == type(other)
                and self.get_parameters() == other.get_parameters()
            )
        else:
            return NotImplemented

    def __hash__(self: Task[T]) -> int:
        return hash(frozenset(self.get_parameters().items()))

    @lru_cache
    def get_dependencies(self: Task[T], *, recurse: bool = False) -> Set[Task]:
        if recurse:
            dependencies = self.get_dependencies(recurse=False)
            while True:
                expanded = dependencies | set(
                    reduce(
                        or_,
                        (
                            x.get_dependencies(recurse=False)
                            for x in dependencies
                        ),
                        set(),
                    ),
                )
                if expanded.issubset(dependencies):
                    return dependencies
                else:
                    dependencies = dependencies | expanded
        else:
            try:
                dependencies, _ = self._dependencies_and_parameters
            except AttributeError:
                return set()
            else:
                return dependencies

    def get_parameters(self: Task[T]) -> Dict[str, Hashable]:
        try:
            _, parameters = self._dependencies_and_parameters
        except AttributeError:
            return {}
        else:
            return parameters

    @classmethod
    def _check_hashable(cls: Type[Task], key: str, value: Any) -> Hashable:
        try:
            hash(value)
        except TypeError:
            raise UnhashableParameterError(
                f"Parameter {cls.__name__}.{key}={value} is not hashable",
            ) from None
        else:
            return value
