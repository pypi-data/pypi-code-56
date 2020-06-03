from collections import abc, defaultdict
from typing import Any, Iterable, Iterator, Mapping, Tuple, Union


class StatefulMapping(abc.Mapping):

    __slots__ = "_state"

    def __init__(self, state: Mapping[Any, Any], /) -> None:
        self._state = state

    def clear(self) -> None:
        self._state.clear()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._state)

    def __len__(self) -> int:
        return len(self._state)


# TODO: Add directed/undirected edges
class network(StatefulMapping):

    _default_edge = _default_vertex = dict

    __slots__ = "_edges", "_vertices"

    def __init__(self) -> None:
        super().__init__(defaultdict(lambda: defaultdict(set)))
        self._edges = defaultdict(self._default_edge)
        self._vertices = defaultdict(self._default_vertex)

    def add_edge(self, edge: Any, /, source_vertex: Any, target_vertex: Any, **data: Any) -> None:
        if not (source_vertex in self._vertices and target_vertex in self._vertices):
            raise KeyError
        if edge not in self._edges:
            self._state[source_vertex][target_vertex].add(edge)
        self._edges[edge].update(data)

    def add_edges(self, e: Iterable[Tuple[Tuple[Any, Any], Iterable[Any]]], /) -> None:
        for vertices, edges in e:
            for edge in edges:
                self.add_edge(edge, *vertices)

    def add_vertex(self, vertex: Any, /, **data: Any):
        self._state[vertex]
        self._vertices[vertex].update(data)

    def add_vertices(self, v: Iterable[Any], /) -> None:
        for vertex in v:
            self.add_vertex(vertex)

    def remove_edge(self, edge: Any, /, source_vertex: Any, target_vertex: Any) -> None:
        if source_vertex in self._vertices and target_vertex in self._state[source_vertex] and edge in self._state[source_vertex][target_vertex]:
            self._state[source_vertex][target_vertex].remove(edge)
            del self._edges[edge]
            if not self._state[source_vertex][target_vertex]:
                del self._state[source_vertex][target_vertex]

    def remove_edges(self, e: Iterable[Tuple[Tuple[Any, Any], Iterable[Any]]], /) -> None:
        for vertices, edges in e:
            for edge in edges:
                self.remove_edge(edge, *vertices)

    def remove_vertex(self, vertex: Any, /) -> None:
        if vertex in self._vertices:
            del self._state[vertex]
            del self._vertices[vertex]
            for source_vertex, neighbors in self._state.items():
                for target_vertex in neighbors:
                    if target_vertex is vertex:
                        del self._state[source_vertex][target_vertex]

    def remove_vertices(self, v: Iterable[Any], /) -> None:
        for vertex in v:
            self.remove_vertex(vertex)

    def edges(self, data=False) -> Union[Mapping[Any, Mapping[str, Any]], Iterable[Any]]:
        return dict(self._edges) if data else set(self._edges)

    def vertices(self, data=False) -> Union[Mapping[Any, Mapping[str, Any]], Iterable[Any]]:
        return dict(self._vertices) if data else set(self._vertices)

    def __getitem__(self, vertex: Any) -> Mapping[Any, Iterable[Any]]:
        if vertex not in self._vertices:
            raise KeyError
        return dict(self._state[vertex])


if __name__ == "__main__":

    def profile(func=None, number=1, sort="cumtime", verbose=False):

        import cProfile
        from functools import wraps, partial

        if not func:
            return partial(profile, number=number, sort=sort, verbose=verbose)

        pr = cProfile.Profile()
        rets = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(number):
                pr.enable()
                ret = func(*args, **kwargs)
                pr.disable()
                rets.append(ret)
                if verbose:
                    pr.print_stats(sort)
            return rets

        return wrapper

    G = network()

    profile(G.add_vertices, verbose=False)(range(100))
    profile(G.add_edges, verbose=False)(((j, j), reversed(list(range(j + 1)))) for j in range(100))

    print(G)
