from .base import BaseQuerySampler
import numpy as np
import pandas as pd


class AlipyWrapper(BaseQuerySampler):

    def __init__(self, estimator, alipy_class, batch_size, train_idx=False):
        super().__init__(batch_size=batch_size)
        self.estimator = estimator
        self.alipy_class = alipy_class
        # For some reason this is needed by some query samplers
        self.train_idx = train_idx

    def fit(self, X, y):

        # Alipy object requires to have access to the whole data.
        # UGLY We store it, no other choice.

        self.X_train = X
        self.y_train = y

    def select_samples(self, X):

        # Alipy crashes if the number of samples to select is the same as the number
        # of samples. We avoid this by preemptively answer this request
        if X.shape[0] == self.batch_size:
            return np.ones(X.shape[0], dtype=int)

        # Alipy do its selection on the whole dataset. Merging train and test:
        n_train, n_test = self.X_train.shape[0], X.shape[0]
        X = np.vstack([self.X_train, X])
        # y is of shape n_train + n_test, we fill the test samples with 0 for each class
        y = np.hstack([self.y_train, np.zeros(n_test)])

        kwargs = dict()
        if self.train_idx:
            kwargs['train_idx'] = np.arange(n_train + n_test)

        selected = self.alipy_class(X, y, **kwargs).select(
            np.arange(n_train),  # Indices of labeled samples
            np.arange(n_train, n_train + n_test),  # Indices of unlabeled samples
            model=self.estimator,
            batch_size=self.batch_size)

        selected = np.asarray(selected) - n_train

        return selected
