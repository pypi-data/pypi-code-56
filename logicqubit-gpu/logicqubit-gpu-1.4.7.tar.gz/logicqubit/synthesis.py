#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

import sympy as sp
from sympy.physics.quantum import TensorProduct
import numpy as np
import cupy as cp

from logicqubit.utils import *

class DecompositionPauliGates:

    def __init__(self, H):
        self.H = H  # hermitian matrix

    def sigma(self):
        ID = np.array([[1, 0], [0, 1]])
        X = np.array([[0, 1], [1, 0]])
        Y = np.array([[0, -1j], [1j, 0]])
        Z = np.array([[1, 0], [0, -1]])
        return [ID, X, Y, Z]

    def get_a(self):
        a = [[0]*4 for i in range(4)]
        for i, sigma_i in enumerate(self.sigma()):
            for j, sigma_j in enumerate(self.sigma()):
                a[i][j] = np.dot(np.kron(sigma_i, sigma_j), self.H).trace()
        return a