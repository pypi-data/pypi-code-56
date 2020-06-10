import numpy as np
import unittest

from research.algorithm.research_algorithm import ResearchEstimator


class TestResearchEstimator(unittest.TestCase):

    def test_predict(self):
        multiplier = 3
        input_data = np.random.random([1, 2])
        expected_result = input_data * multiplier
        estimator = ResearchEstimator(multiplier=multiplier)
        result = estimator.predict(input_data)

        self.assertTrue(np.allclose(result, expected_result))
