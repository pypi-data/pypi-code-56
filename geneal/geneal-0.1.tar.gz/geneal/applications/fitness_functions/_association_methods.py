from functools import reduce
from itertools import combinations

import numpy as np
from dcor import distance_correlation
from numba import njit, jit
from scipy.stats import pearsonr


association_methods = {
    "DCD": {"association_method": distance_correlation, "relation": "difference"},
    "DCQ": {"association_method": distance_correlation, "relation": "quotient"},
    "PCD": {
        "association_method": lambda x, y: np.abs(pearsonr(x, y)[0]),
        "relation": "difference",
    },
    "PCQ": {
        "association_method": lambda x, y: np.abs(pearsonr(x, y)[0]),
        "relation": "quotient",
    },
}


class AssociationMethods:
    def __init__(self, features, target, method: str = "DCD"):

        if method not in association_methods:
            raise Exception(
                f"Invalid method, must be one of {association_methods}."
                f" Check the documentation for more details"
            )

        if target.ndim != 1:
            raise Exception(f"Invalid target variable, it must be a 1-D array")

        self.features = np.array(features)
        self.target = np.array(target)

        self.association_method = association_methods[method]["association_method"]
        self.relation = association_methods[method]["relation"]

    def fitness_function(self, individual):

        on_features = np.arange(self.features.shape[1])[individual == 1]

        relevance = reduce(
            lambda prev, feature: prev
            + np.nan_to_num(
                self.association_method(self.features[:, feature], self.target)
            ),
            on_features,
            0,
        )

        redundancy = reduce(
            lambda prev, case: prev
            + np.nan_to_num(
                self.association_method(
                    self.features[:, case[0]], self.features[:, case[1]]
                )
            ),
            combinations(on_features, 2),
            0,
        )

        cardinality = on_features.size

        try:
            if self.relation == "difference":
                return relevance / cardinality - redundancy / cardinality ** 2
            else:
                return (relevance / cardinality) / (redundancy / cardinality ** 2)
        except ZeroDivisionError:
            return 0
