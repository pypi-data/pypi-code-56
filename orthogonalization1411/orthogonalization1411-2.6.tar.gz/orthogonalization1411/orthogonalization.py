import numpy as np
import pandas as pd


class Orthogonalization:
    
    def __init__(self, factors):
        self.factors = factors
        
    def schimidt(self):
        """
        施密特正交
        :param factors:
        :return:
        """
        R = np.zeros((self.factors.shape[1], self.factors.shape[1]))
        Q = np.zeros(self.factors.shape)
        for k in range(0, self.factors.shape[1]):
            R[k, k] = np.sqrt(np.dot(self.factors[:, k], self.factors[:, k]))
            Q[:, k] = self.factors[:, k] /R[k, k]
            for j in range(k + 1, self.factors.shape[1]):
                R[k, j] = np.dot(Q[:, k], self.factors[:, j])
                self.factors[:, j] = self.factors[:, j] - R[k, j] *Q[:, k]
        return Q

    def canonial(self):
        """
        规范正交
        :param factors:
        :return:
        """
        D, U = np.linalg.eig(np.dot(self.factors.T, self.factors))
        S = np.dot(U, np.diag(D ** (-0.5)))
        return np.dot(self.factors, S)

    def symmetry(self):
        """
        对称正交
        :param factors:
        :return:
        """
        D, U = np.linalg.eig(np.dot(self.factors.T, self.factors))  # 特征值，特征向量
        D = np.diag(D)
        try:
            D = np.linalg.inv(D)
        except:  # 奇异矩阵
            D = np.linalg.pinv(D)
        S = U.dot(np.sqrt(D)).dot(U.T)
        return np.dot(self.factors, S)



