from numpy import *
from .activation import Activation

class Sigmoid(Activation):
    __withActivation__ = True
    @staticmethod
    def __call__(x,back=False):
        if not back:
            return Sigmoid.__Pass__(x)
        return Sigmoid.__getDerivative__(x)
    def __Pass__(x):
        return 1/(1+e**-x)
    def __getDerivative__(x):
        x = array(x)
        return x*(1-x)

class Linear(Activation):
    __withActivation__ = False
    @staticmethod
    def __call__(x,back=False):
        if not back:
            return Linear.__Pass__(x)
        return Linear.__getDerivative__()
    def __Pass__(x):
        return x
    def __getDerivative__():
        return 1

class Relu(Activation):
    __withActivation__ = False
    @staticmethod
    def __call__(x,back=False):
        if not back:
            return Relu.__Pass__(x)
        return Relu.__getDerivative__(x)
    def __Pass__(x):
        return maximum(0,x)
    def __getDerivative__(x):
        return array(list(map(lambda x: 1 if x > 0 else 0,x)))
