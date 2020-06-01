from collections import defaultdict, namedtuple
from typing import Any, List, Mapping, FrozenSet, Set, Tuple, Union


__all__ = ["network"]


# TODO: Implement edge directed property
class network(defaultdict):
    """Network science abstract data type

    Extends:
        defaultdict
    """

    # TODO: Create DictList data structure to be able to store multiple edges pointing to same target vertex
    class __adj(defaultdict):
        """Adjacency list

        Extends:
            defaultdict
        """

        def __init__(self, network: "network", source_vertex: Any = None) -> None:
            """Initialize new adjacency list

            Arguments:
                network {network}
                source_vertex {Any}
            """
            super().__init__(lambda: network.default_edge)
            self.__network = network
            self.__source_vertex = source_vertex

        @property
        def source_vertex(self) -> Any:
            """Return adjacency list source vertex

            Returns:
                Any
            """
            return self.__source_vertex

        @source_vertex.setter
        def source_vertex(self, source_vertex: Any) -> None:
            """Override previous source vertex adjacency list and set new adjacency list source vertex

            Arguments:
                source_vertex {Any}
            """
            if self.__source_vertex in self.__network:
                self.__network[self.__source_vertex] = network._network__adj(self.__network, self.__source_vertex)
            self.__network[source_vertex] = self
            self.__source_vertex = source_vertex

        def __getitem__(self, target_vertex: Any) -> Mapping[str, Any]:
            """Create new vertex if vertex not in network and edge if edge not in adjacency list and return vertex edge

            Arguments:
                target_vertex {Any}

            Returns:
                Mapping[str, Any]
            """
            self.__network[target_vertex]
            return super().__getitem__(target_vertex)

        def __setitem__(self, vertex: Any, edge: Mapping[str, Any]) -> None:
            """Create new vertex if vertex not in network and edge if edge not in adjacency list and set vertex edge

            Arguments:
                vertex {Any}
                edge {Mapping[str, Any]}

            Raises:
                TypeError: if edge not of type Mapping[str, Any]
            """
            try:
                dict(**edge)
            except TypeError as e:
                raise TypeError(f"'edge: {edge}' not of type 'Mapping[str, Any]'...") from e
            self.__network[vertex]
            super().__setitem__(vertex, edge)

        def __repr__(self) -> str:
            """Return adjacency list dictionary representation

            Returns:
                str
            """
            return dict.__repr__(self)

    def __init__(self, default_vertex: Mapping[str, Any] = dict(), default_edge: Mapping[str, Any] = dict()) -> None:
        """Initialize new network

        Keyword Arguments:
            default_vertex {Mapping[str, Any]} -- (default: {dict()})
            default_edge {Mapping[str, Any]} -- (default: {dict()})
        """
        super().__init__(lambda vertex: network.__adj(self, vertex))
        self.__vertices = dict()
        self.__edges = dict()
        self.default_vertex = default_vertex
        self.default_edge = default_edge

    # TODO: Implement
    def subgraph(self, vertices=list(), edges=list()):
        pass

    def clear(self) -> None:
        """Remove network vertices and edges
        """
        super().clear()
        self.__vertices.clear()
        self.__edges.clear()

    def pop(self, vertex: Any, default: Any = None) -> Any:
        """Return deleted vertex from network or default if vertex not in network

        Arguments:
            vertex {Any}

        Keyword Arguments:
            default {Any} -- (default: {None})

        Returns:
            Any
        """
        if vertex in self:
            del self[vertex]
            return vertex
        return default

    def popitem(self) -> Tuple[Any, Mapping[str, Any]]:
        """Return deleted vertex adjacency list pair from network in LIFO order

        Raises:
            KeyError: if not network

        Returns:
            Tuple[Any, Mapping[str, Any]]
        """
        if not self:
            raise KeyError("'network' is empty...")
        vertex, adj = next(reversed(self.items()))
        del self[vertex]
        return vertex, adj

    # TODO: Implement
    def setdefault(self, data, default=None):
        if data in self.values():
            return data
        return default

    # TODO: Implement
    def update(self, vertices=None, edges=None):
        super().update()

    def get_vertices(self, data: bool = False) -> Union[Mapping[Any, Mapping[str, Any]], List[Any]]:
        """Return network vertices

        Keyword Arguments:
            data {bool} -- (default: {False})

        Returns:
            Union[Mapping[Any, Mapping[str, Any]], List[Any]]
        """
        return dict(self.__vertices) if data else list(self.__vertices.keys())

    def del_vertices(self) -> None:
        """Delete network vertices data
        """
        self.__vertices.update(dict.fromkeys(self.__vertices, self.__default_vertex))

    # TODO: Fix
    def get_edges(self, data: bool = False) -> Union[Mapping[Tuple[Any, Any], Mapping[str, Any]], List[Tuple[Any, Any]]]:
        """Return network edges

        Keyword Arguments:
            data {bool} -- (default: {False})

        Returns:
            Union[Mapping[Tuple[Any, Any], Mapping[str, Any]], Set[Tuple[Any, Any]]]
        """
        Edge = namedtuple("Edge", "source_vertex target_vertex")
        edges = dict() if data else set()
        for v, e in self.items():
            for u in e:
                edges.update({Edge(v, u): e[u]}) if data else edges.add(Edge(v, u))
        return edges

    def del_edges(self) -> None:
        """Delete network edge data
        """
        # self.__edges.update(dict.fromkeys(self.__edges, self.__default_edge))
        for edge in self.values():
            edge.update(dict.fromkeys(edge, self.__default_edge))

    @property
    def default_vertex(self) -> Mapping[str, Any]:
        """Return default vertex

        Returns:
            Mapping[str, Any]
        """
        return self.__default_vertex

    @default_vertex.setter
    def default_vertex(self, default_vertex: Mapping[str, Any]) -> None:
        """Set default vertex

        Arguments:
            default_vertex {Mapping[str, Any]}

        Raises:
            TypeError: if default_vertex not of type Mapping[str, Any]
        """
        try:
            self.__default_vertex = dict(**default_vertex)
        except TypeError as e:
            raise TypeError(f"'default_edge: {default_vertex}' not of type 'Mapping[str, Any]'...") from e

    @property
    def default_edge(self) -> Mapping[str, Any]:
        """Return default edge

        Returns:
            Mapping[str, Any]
        """
        return self.__default_edge

    @default_edge.setter
    def default_edge(self, default_edge: Mapping[str, Any]) -> None:
        """Set default edge

        Arguments:
            default_edge {Mapping[str, Any]}

        Raises:
            TypeError: if default_edge not of type Mapping[str, Any]
        """
        try:
            self.__default_edge = dict(**default_edge)
        except TypeError as e:
            raise TypeError(f"'default_edge: {default_edge}' not of type 'Mapping[str, Any]'...") from e

    def __setitem__(self, vertex: Any, data: Mapping[str, Any]) -> None:
        """Create new vertex if not in network and set vertex data

        Arguments:
            vertex {Any}
            data {Mapping[str, Any]}

        Raises:
            TypeError: if data not of type Mapping[str, Any]
        """
        if isinstance(data, self.__adj):
            super().__setitem__(vertex, data)
            self.__vertices[vertex] = self.__default_vertex
        else:
            try:
                self[vertex]
                self.__vertices[vertex] = dict(**data)
            except TypeError as e:
                raise TypeError(f"'data: {data}' not of type 'Mapping[str, Any]'...") from e

    def __delitem__(self, vertex: Any) -> None:
        """Delete vertex from network

        Arguments:
            vertex {Any}

        Raises:
            KeyError: if vertex not in network
        """
        try:
            super().__delitem__(vertex)
            del self.__vertices[vertex]
            for source_vertex, target_vertex in self.edges:
                if target_vertex is vertex:
                    del self[source_vertex][target_vertex]
        except KeyError as e:
            raise KeyError(f"'vertex: {vertex}' not in 'network'...") from e

    def __missing__(self, vertex: Any) -> Mapping[str, Any]:
        """Create new adjacency list and return vertex adjacency list

        Arguments:
            vertex {Any}

        Raises:
            KeyError: if default_factory is None

        Returns:
            Mapping[str, Any]
        """
        if self.default_factory is None:
            raise KeyError(vertex)
        self[vertex] = self.default_factory(vertex)  # pylint: disable=not-callable
        return self[vertex]

    def __repr__(self) -> str:
        """Return network attribute representation

        Returns:
            str
        """
        return f"{self.__class__.__name__}(<{self.__default_vertex=}, {self.__default_edge=}>, {self})"

    def __str__(self) -> str:
        """Return network dictionary representation

        Returns:
            str
        """
        return dict.__repr__(self)

    vertices = property(fget=get_vertices, fdel=del_vertices)
    edges = property(fget=get_edges, fdel=del_edges)


if __name__ == "__main__":
    # Test
    G = network()
