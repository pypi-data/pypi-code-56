import re
import networkx as nx
import pydotplus
import warnings

"""
VeazyHelper is built around two assumptions:
* A function name never contains '__' within the function name 
    (though at start/end is fine, like __init__)
* A function name never contains '___'

Our dependency pyan3 doesn't like relative imports
"""


class Veazy:
    # TODO: refactor names, e.g. source_file -> root file; method names
    def __init__(self, pyg, source_file):
        self.pyg = pyg
        self.depth_of_nodes = []
        self.nodes_to_deep = []
        self.edges_to_deep = []
        self.node_list = []
        self.script_nodes = []

        self._fill_filter_node_list()
        if source_file == "":
            raise Exception("Please provide a root file")
        try:
            self.top_node = re.sub(".py", "", source_file)
            self._fill_depth_of_nodes()
        except nx.exception.NodeNotFound:
            raise ValueError(
                "The supplied root file does not call any "
                "methods or functions in the supplied graph"
            )

    def _fill_filter_node_list(self):
        self.node_list = []
        self._fill_node_list(self.pyg)
        self.node_list = self._filter_node_list(self.node_list)
        self.script_nodes = list(
            self.pyg.get_subgraph_list()[0].obj_dict["nodes"].keys()
        )

    def _fill_node_list(self, graph):
        self.node_list = self.node_list + list(graph.obj_dict["nodes"].keys())
        for subgraph in graph.get_subgraph_list():
            self._fill_node_list(subgraph)

    def _filter_node_list(self, node_list):
        # TODO: static method, move to helper module?
        # TODO feels a bit over the top to put this in a function
        return set([node for node in node_list if node != "graph"])

    def _fill_depth_of_nodes(self):
        self.depth_of_nodes = []

        # utilize networkx to calculate depth
        nxg = nx.drawing.nx_pydot.from_pydot(self.pyg)

        # calculate depth of nodes, based on first node
        self.depth_of_nodes = dict(
            nx.single_source_shortest_path_length(nxg, self.top_node)
        )
        missing_depths = {}
        for node in self.node_list:
            if node not in self.depth_of_nodes.keys():
                # TODO: These are scripts. Put in init or something?
                if node in self.script_nodes:
                    missing_depths[node] = 0
                else:
                    # TODO: does this work correctly, and do we want this `here`?
                    self._delete_node_edge([node])
        self.depth_of_nodes = {**self.depth_of_nodes, **missing_depths}

    def _split_func_str(self, func_str):
        # TODO: static method, move to helper module?
        """
        :param func_str: e.g. "bacon__eggs"
        :return: ("bacon", "eggs")
        """
        # derive the number of functions in the func_str
        n_func = len([sub_func for sub_func in func_str.split("__") if sub_func != ""])
        # construct regex pattern based on number of functions
        # this ensures that we have enough regex capture groups
        # (regex's own repeat pattern functionality didn't work well in this respect)
        regex_pattern_partial = "(__.*[^_]__|.*[^_])"
        regex_pattern = "__".join([regex_pattern_partial] * n_func)
        # make sure output is tuple
        split_func = re.findall(regex_pattern, func_str)[0]
        if type(split_func) == str:
            split_func = tuple([split_func])
        return split_func

    def _find_edges(self, nodes_to_search):
        """
        :param nodes_to_search: list of node names (str)
        :param originating_from_node:
            if true, function will return edges originating from nodes
            if false, function will return edges pointing at nodes
        :return: list of edge tuples
        """
        return [
            edge
            for edge in self.pyg.obj_dict["edges"].keys()
            if any(i in nodes_to_search for i in edge)
        ]

    def _delete_node_edge(self, nodes):
        def del_node_recursive(graph, node):
            # TODO: static method, move to helper module?
            """
            :param graph: a graph in which to delete nodes and look for subgraphs
            :param node: node name (str)
            """
            graph.del_node(node)
            # repeat for every subgraph in self.pyg (recursively)
            for subgraph in graph.get_subgraph_list():
                del_node_recursive(subgraph, node)

        for node in nodes:
            del_node_recursive(self.pyg, node)
        for edge in self._find_edges(nodes):
            self.pyg.del_edge(edge)
        self._fill_filter_node_list()

    def _fill_to_deep(self, max_depth):
        self.nodes_to_deep = []
        self.edges_to_deep = []

        self.nodes_to_deep = [
            node for node, depth in self.depth_of_nodes.items() if depth > max_depth
        ]
        self.edges_to_deep = self._find_edges(self.nodes_to_deep)

    def _find_scripts(self):
        nodes_from_script = self._filter_node_list(self.script_nodes)
        nodes_from_script = [i for i in nodes_from_script if i != self.top_node]
        return nodes_from_script

    def _add_summarizing(self, max_depth):
        # TODO: split code?
        # TODO: can we prevent summarizing nodes of size 1?
        def find_cluster(graph, cluster):
            """
            :param graph: a graph in which to search for cluster and look for subgraphs
            :param cluster: cluster name (str)
            """
            if cluster[:8] != "cluster_":
                cluster = "cluster_" + cluster
            if graph.obj_dict["name"] == cluster:
                return graph
            # repeat for every subgraph in graph (recursively)
            for subgraph in graph.get_subgraph_list():
                result = find_cluster(subgraph, cluster)
                if result:
                    return result

        # From the deleted nodes, find level that is not to deep.
        # This level will be re-added as summarizing node.
        def get_summarized_name(node):
            # TODO: follow-up on -r cli.py -d 4 cli.py veazy.py
            #  _split_func_str seems deeper than it is, because we look at the depth
            #  of the node with regards to the call graph
            #  rather than looking at the parent graph
            summarized_node = "__".join(
                self._split_func_str(node)[
                    : (
                        len(self._split_func_str(node))
                        - (self.depth_of_nodes[node] - max_depth)
                    )
                ]
            )
            if summarized_node != node:
                summarized_node = "SUMMARIZED_FROM_" + summarized_node
            return summarized_node

        summarizing_nodes = set(
            [get_summarized_name(node) for node in self.nodes_to_deep]
        )
        summarizing_edges = []
        for edge in self.edges_to_deep:
            summarizing_edges.append(
                (get_summarized_name(edge[0]), get_summarized_name(edge[1]),)
            )
        # TODO: is this working as expected?
        summarizing_edges = [
            edge
            for edge in summarizing_edges
            if all([i in summarizing_nodes or i in self.node_list for i in edge])
        ]
        for node in summarizing_nodes:
            if node != "":
                add_to_graph = find_cluster(self.pyg, node.split("SUMMARIZED_FROM_")[1])
                # TODO: can `if` below be incorporated into recursive function?
                if not add_to_graph:
                    add_to_graph = self.pyg
                add_to_graph.add_node(pydotplus.graphviz.Node(name=node))
        for edge in set(summarizing_edges):
            if "" not in edge:
                self.pyg.add_edge(pydotplus.graphviz.Edge(src=edge[0], dst=edge[1]))
        # TODO: There are quite a few functions where this is called at the end.
        #  Rewrite to decorator?
        self._fill_filter_node_list()

    def _add_final_summarizing(self):
        if len(self.edges_to_deep) > 0:
            self.pyg.get_subgraph_list()[0].add_node(
                pydotplus.graphviz.Node(name="...")
            )
        summarizing_edges = []
        for edge in self.edges_to_deep:
            e0 = edge[0] if edge[0] not in self.nodes_to_deep else "..."
            e1 = edge[1] if edge[1] not in self.nodes_to_deep else "..."
            summarizing_edges.append((e0, e1))
        summarizing_edges = set(
            [
                edge
                for edge in summarizing_edges
                if not all([node == "..." for node in edge])
            ]
        )
        for edge in summarizing_edges:
            self.pyg.add_edge(pydotplus.graphviz.Edge(src=edge[0], dst=edge[1]))
        self._fill_filter_node_list()

    def prune_depth(self, max_depth):
        if max_depth < 1:
            warnings.warn(
                f"The max_depth that was passed({max_depth}) will be ignored, "
                "and set to the minimum value of 1"
            )
        max_depth = max(1, max_depth - 1)
        self._fill_depth_of_nodes()
        self._fill_to_deep(max_depth)
        self._delete_node_edge(self.nodes_to_deep)
        self._delete_node_edge(self._find_scripts())
        self._add_summarizing(max_depth)

        self._fill_depth_of_nodes()
        self._fill_to_deep(max_depth + 1)
        self._delete_node_edge(self.nodes_to_deep)
        self._delete_node_edge([self.top_node])
        # TODO: -r cli.py -d 4 cli.py veazy.py
        #  causes a ... node to be made, whereas the ... node is actually the same
        #  as an already present summarizing node
        self._add_final_summarizing()
        return self.pyg

    def _find_depth_from_nodes(self, max_nodes):
        # TODO: can we break this?
        def depth_from_nodes(depth):
            return sum([i < depth for i in self.depth_of_nodes.values() if i != 0])

        max_depth = 1
        while depth_from_nodes(max_depth) < max_nodes:
            max_depth += 1
            if max_depth == (max(self.depth_of_nodes.values()) + 1):
                break
        if abs(depth_from_nodes(max_depth - 1) - max_nodes) < abs(
            depth_from_nodes(max_depth) - max_nodes
        ):
            max_depth -= 1
        return max_depth

    def find_auto_depth(self):
        return self._find_depth_from_nodes(30)

    def prune_width(self, max_nodes):
        max_depth = self._find_depth_from_nodes(max_nodes)
        return self.prune_depth(max_depth)

    def prune_auto(self):
        max_depth = self.find_auto_depth()
        return self.prune_depth(max_depth)
