import numpy as np
from numpy.testing import assert_array_equal
import pytest
from cardinal.version import check_modules

#if check_modules('sklearn', 'clustering', strict=False):  # noqa
#    pytest.skip('sklearn option seems not installed. Skipping test.',  # noqa
#        allow_module_level=True)  # noqa

from cardinal.clustering import KCentroidSampler


class DoNothing():

    def fit(self, X, y=None, sample_weight=None):
        return self

    def transform(self, X):
        return X


def test_kmeans_with_conflict():

    distances = np.array([[0.10, 0.25, 0.30],
                          [0.25, 0.10, 0.10],
                          [0.30, 0.30, 0.20],
                          [0.40, 0.40, 0.40]])

    # In this configuration, sample 2 (1-indexed) is the closest
    # to the center of clusters 2 and 3. In this case, we want to
    # select sample 3 for cluster 3

    sampler = KCentroidSampler(DoNothing(), batch_size=3)
    selected = sampler.fit(None).select_samples(distances)
    assert_array_equal(np.sort(selected), np.array([0, 1, 2]))