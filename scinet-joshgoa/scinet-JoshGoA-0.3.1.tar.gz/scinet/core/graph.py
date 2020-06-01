from collections import abc
from typing import Any, Iterable, Mapping, Tuple, Union
from warnings import warn


__all__ = ["Graph"]


class Graph(abc.Mapping):

    __slots__ = "_adj"

    def __init__(self) -> None:
        self._adj = dict()

    def add_vertex(self, vertex: Any, /) -> None:
        if vertex not in self._adj:
            self._adj[vertex] = {}

    def add_edge(self, edge: Any, /, source_vertex: Any, target_vertex: Any) -> None:
        for vertex in {source_vertex, target_vertex}:
            self.add_vertex(vertex)
        if target_vertex not in self._adj[source_vertex]:
            self._adj[source_vertex][target_vertex] = []
        self._adj[source_vertex][target_vertex].append(edge)

    def remove_vertex(self, vertex: Any, /) -> None:
        try:
            del self._adj[vertex]
            for source_vertex, neighbors in self._adj.items():
                for target_vertex in neighbors:
                    if target_vertex is vertex:
                        del self._adj[source_vertex][target_vertex]
        except KeyError:
            warn(f"'{vertex=}' not in '{self.__class__.__name__}'...")

    def remove_edge(self, edge: Any, /, source_vertex: Any, target_vertex: Any) -> None:
        try:
            self._adj[source_vertex][target_vertex].remove(edge)
            if not self._adj[source_vertex][target_vertex]:
                del self._adj[source_vertex][target_vertex]
        except KeyError:
            warn(f"'{edge=} not in '{self.__class__.__name__}'...")

    def __getitem__(self, vertex: Any, /) -> Any:
        return dict(self._adj[vertex])

    def __iter__(self) -> None:
        return iter(self._adj)

    def __len__(self) -> int:
        return len(self._adj)

    def __str__(self) -> str:
        return str(self._adj)
