import numpy as np


def linear(x, a, b):
    return a*x + b


def expfunc(x, a, b, c):
    return a * np.exp(-b * x) + c


def expfuncinv(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c


def log(x, a, b):
    return a*np.log(x) + b


def sigmoid(x, s=1, a=0, b=1):
    return b/(1 + np.exp(-s*(x - a)))


def sigmoid_inverse(x, s=1, a=0, b=1):
    return 1.0 - b/(1 + np.exp(-s*(x - a)))
