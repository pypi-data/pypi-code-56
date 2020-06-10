import numpy as np
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger('k_mxt_w3.clusters_data')


class ClustersData(ABC):
    cluster_numbers = None
    num_of_data = 0
    data_ration = None

    @staticmethod
    def array_rationing(array):
        return (array - np.mean(array)) / np.std(array)

    @abstractmethod
    def distance(self, point: np.ndarray):
        pass

    @abstractmethod
    def get_cluster_name(self, cluster_num):
        if self.cluster_numbers is None:
            raise TypeError('self.cluster_numbers does not equal None')


class MetricsMixin:
    data_ration = None
    time_init = None
    factor = None

    def euclidean_distance(self, point1, point2=None):
        def euclidean_distance_between_point_array(num_point):
            return np.sqrt(np.sum((self.data_ration - self.data_ration[num_point]) ** 2, axis=1))

        def euclidean_distance_between2points(point1, point2):
            return np.sqrt(np.sum((self.data_ration[point1] - self.data_ration[point2]) ** 2))

        if point2 is None:
            return euclidean_distance_between_point_array(num_point=point1)
        else:
            return euclidean_distance_between2points(point1=point1, point2=point2)

    def euclidean_distance_using_factor(self, point1, point2=None):
        def euclidean_distance_between_point_array(num_point):
            return np.sqrt(np.sum(((self.data_ration - self.data_ration[num_point]) * self.factor) ** 2, axis=1))

        def euclidean_distance_between2points(point1, point2):
            return np.sqrt(np.sum(((self.data_ration[point1] - self.data_ration[point2]) * self.factor) ** 2))

        if point2 is None:
            return euclidean_distance_between_point_array(num_point=point1)
        else:
            return euclidean_distance_between2points(point1=point1, point2=point2)


class ClustersDataSpace(ClustersData, ABC):
    def __init__(self, x_init: np.ndarray, y_init: np.ndarray):
        if x_init.shape != y_init.shape:
            raise ValueError('x_init and y_init must be the same dimension')
        self.x_init = x_init.copy()
        self.y_init = y_init.copy()
        self.data_ration = None
        self.cluster_numbers = np.full(len(self.x_init), -1)
        self.num_of_data = self.x_init.shape[0]


class ClustersDataSpaceEuclidean(MetricsMixin, ClustersDataSpace):
    def __init__(self, x_init: np.ndarray, y_init: np.ndarray):
        super().__init__(x_init, y_init)
        self.data_ration = np.array([self.x_init,
                                     self.y_init]).transpose()

    def distance(self, point1, point2=None):
        return self.euclidean_distance(point1, point2)

    def get_cluster_name(self, cluster_num):
        super().get_cluster_name(cluster_num)
        return str(cluster_num)


class ClustersDataSpaceFeatures(ClustersDataSpace, ABC):

    def __init__(self, x_init: np.ndarray, y_init: np.ndarray, features_init: np.ndarray):
        """
        :param x_init:
        :param y_init:
        :param features_init: each row corresponds to a single data point.
        """
        super().__init__(x_init, y_init)
        self.features_init = features_init.copy()
        self.data_ration = np.concatenate((ClustersData.array_rationing(self.x_init),
                                           ClustersData.array_rationing(self.y_init),
                                           ClustersData.array_rationing(self.features_init)), axis=1)

    def get_cluster_name(self, cluster_num):
        pass


class ClustersDataSpaceFeaturesEuclidean(MetricsMixin, ClustersDataSpaceFeatures):
    def __init__(self, x_init: np.ndarray, y_init: np.ndarray, features_init: np.ndarray):
        super().__init__(x_init, y_init, features_init)

    def distance(self, point1, point2=None):
        return self.euclidean_distance(point1, point2)
