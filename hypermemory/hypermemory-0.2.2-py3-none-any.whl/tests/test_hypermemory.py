# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import time
import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import WhiteKernel, ConstantKernel, RBF

from hypermemory import Hypermemory


def test_int_IO():
    data = load_iris()
    X, y = data.data, data.target

    def model(para, X, y):
        dtc = DecisionTreeClassifier(
            max_depth=para["max_depth"], min_samples_split=para["min_samples_split"],
        )
        scores = cross_val_score(dtc, X, y, cv=3)

        return scores.mean()

    search_space = {
        "max_depth": range(1, 5),
        "min_samples_split": range(10, 50),
    }

    memory_in = {
        (1, 2): {"score": 1, "eval_time": 1},
        (2, 3): {"score": 1, "eval_time": 1},
    }

    mem = Hypermemory(X, y, model, search_space)
    mem.dump(memory_in)
    memory_out = mem.load()

    assert memory_in == memory_out


def test_float_IO():
    data = load_iris()
    X, y = data.data, data.target

    def model(para, X, y):
        dtc = MLPClassifier(alpha=para["alpha"])
        scores = cross_val_score(dtc, X, y, cv=3)

        return scores.mean()

    search_space = {
        "alpha": list(np.arange(0.0001, 0.001, 0.0001)),
    }

    memory_in = {
        (1,): {"score": 1, "eval_time": 1},
    }

    mem = Hypermemory(X, y, model, search_space)
    mem.dump(memory_in)
    memory_out = mem.load()

    assert memory_in == memory_out


def test_str_IO():
    data = load_iris()
    X, y = data.data, data.target

    def model(para, X, y):
        dtc = GradientBoostingClassifier(loss=para["loss"])
        scores = cross_val_score(dtc, X, y, cv=3)

        return scores.mean()

    search_space = {
        "loss": ["deviance", "exponential"],
    }

    memory_in = {
        (0,): {"score": 1, "eval_time": 1},
        (1,): {"score": 1, "eval_time": 1},
    }

    mem = Hypermemory(X, y, model, search_space)
    mem.dump(memory_in)
    memory_out = mem.load()

    assert memory_in == memory_out


def test_object_IO():
    data = load_iris()
    X, y = data.data, data.target

    def model(para, X, y):
        dtc = GaussianProcessClassifier(kernel=para["kernel"])
        scores = cross_val_score(dtc, X, y, cv=3)

        return scores.mean()

    search_space = {
        "kernel": [WhiteKernel(), ConstantKernel(), RBF()],
    }

    memory_in = {
        (0,): {"score": 1, "eval_time": 1},
        (1,): {"score": 1, "eval_time": 1},
    }

    mem = Hypermemory(X, y, model, search_space)
    mem.dump(memory_in)
    memory_out = mem.load()

    print("\n memory_out \n", memory_out)

    assert memory_in == memory_out
