"""
"""

from abc import ABC, abstractmethod
import numpy as np

class ConjugateModel(ABC):
    """
    """

    def __init__(self, random_state=np.random, *args, **kwargs):
        """
        """
        super(ConjugateModel, self).__init__(*args, **kwargs)
        self.fitted = False
        self.random_state = random_state

    @abstractmethod
    def sample_prior(self):
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def sample_prior_predictive(self):
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def fit(self):
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def sample_posterior(self):
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def sample_posterior_predictive(self):
        """
        """
        raise NotImplementedError()
