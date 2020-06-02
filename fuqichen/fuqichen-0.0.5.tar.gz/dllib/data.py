import numpy as np

def normalize(data, mean, stddev, eps=np.finfo(float).eps):
    return (data - mean) / (stddev + eps)


def normalize_instance(data, eps=np.finfo(float).eps):
    mean = data.mean()
    std = data.std()
    return normalize(data, mean, std, eps), mean, std
