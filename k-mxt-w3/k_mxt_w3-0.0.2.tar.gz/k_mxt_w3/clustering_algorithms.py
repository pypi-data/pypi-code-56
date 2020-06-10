from abc import ABC
import numpy as np
import copy
import k_mxt_w3.graph
import logging
import scipy.stats

import k_mxt_w3.clusters_data

logger = logging.getLogger('k_mxt_w3.clustering_algorithm')


class Clustering(ABC):
    def __init__(self, clusters_data: k_mxt_w3.clusters_data.ClustersData):
        self.clustersData = copy.deepcopy(clusters_data)


class K_MXT(Clustering):
    def __init__(self, k: int, eps: float, clusters_data: k_mxt_w3.clusters_data.ClustersData):
        logger.info(f'init k-{k}, eps-{eps}, clusters_data-{clusters_data}')
        self.k = k
        self.eps = eps
        self.clusters_data = clusters_data
        self.num_of_vertices = self.clusters_data.num_of_data
        self.start_graph = [None for _ in range(self.num_of_vertices)]
        self.k_graph = [None for _ in range(self.num_of_vertices)]
        logger.info(f'init has done.')

    def make_start_graph(self):
        def get_neighbor(v):
            dst = self.clusters_data.distance(v)
            neighbor = np.where(dst <= self.eps)[0]
            index_v = np.argwhere(neighbor == v)
            self.start_graph[v] = np.delete(neighbor, index_v)

        for v in range(self.clusters_data.num_of_data):
            get_neighbor(v)

    def get_arc_weight(self, v, to):
        return np.intersect1d(self.start_graph[v], self.start_graph[to]).shape[0]

    def make_k_graph(self):
        if any(x is None for x in self.start_graph):
            raise TypeError('self.start_graph do not have to consist None.')
        if not self.eps > 0.0:
            raise ValueError("eps must be positive.")
        np.random.seed(4000)
        edge_weights = None

        def get_k_max_arcs():
            if edge_weights.shape[0] < self.k:
                return edge_weights['vertex']
            edge_weights.sort(order='weight')
            weights = np.flip(edge_weights)
            k_value = weights['weight'][self.k - 1]
            index_k_value = np.where(weights['weight'] == k_value)[0]
            index_k_value_min, index_k_value_max = index_k_value[0], index_k_value[-1]
            np.random.shuffle(weights[index_k_value_min:index_k_value_max+1])
            return weights['vertex'][:self.k]

        for v in range(self.num_of_vertices):
            iterable = ((self.get_arc_weight(v, neighbor), neighbor) for neighbor in self.start_graph[v])
            edge_weights = np.fromiter(iterable, dtype=[('weight', float), ('vertex', int)])
            self.k_graph[v] = get_k_max_arcs()
            edge_weights = None

    def __call__(self, *args, **kwargs):
        logger.info(f'clustering has started')
        logger.info(f'start making start graph')
        self.make_start_graph()
        logger.info(f'start making k-graph')
        self.make_k_graph()
        logger.info(f'start finding scc')
        g = k_mxt_w3.graph.Graph(adj=self.k_graph)
        self.clusters_data.cluster_numbers = np.array(g.find_scc())
        logger.info(f'clustering has finished')


class K_MXT_gauss(K_MXT):
    def __init__(self, k: int, eps: float, clusters_data: k_mxt_w3.clusters_data.ClustersData):
        super().__init__(k=k, eps=eps, clusters_data=clusters_data)
        self.sigma = eps / 3
        self.norm = scipy.stats.norm(0, self.sigma)

    def get_arc_weight(self, v, to):
        return self.norm.pdf(self.clusters_data.distance(v, to)) * super().get_arc_weight(v, to)




