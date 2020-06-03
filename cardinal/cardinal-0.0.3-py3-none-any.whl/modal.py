from .base import BaseQuerySampler
import numpy as np


class ModalWrapper(BaseQuerySampler):

    def __init__(self, learner, batch_size, refit=False):
        super().__init__(batch_size)
        self.learner = learner
        self.refit = refit

    def fit(self, X, y):

        if self.refit:
            self.learner.fit(X, y)
        else:
            self.learner._add_training_data(X, y)

        return self

    def select_samples(self, X):
        selected_idx, _ = self.learner.query(X, n_instances=self.batch_size)
        return selected_idx
