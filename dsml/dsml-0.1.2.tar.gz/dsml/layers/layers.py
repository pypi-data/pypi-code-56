from numpy import *
from .layer import Layer
from ..activations.activations import Linear
import sys
if sys.version_info[0] >= 3:
    from functools import reduce

class Full(Layer):
    def __init__(self,inAmount,activation=Linear):
        self.inAmount = inAmount
        self.activation = activation()

    def __call__(self,x,returnValues=False):
        if not returnValues:
            return self.__passForward__(x)
        return self.__passAndReturn(x)

    def __len__(self):
        return self.inAmount

    def init(self,outAmount,activation):
        self.outAmount = outAmount

        self.weights = random.randn(outAmount,self.inAmount)
        self.biases = random.randn(self.outAmount)

        self.activation = activation
        self.__withActivation__ = self.activation.__withActivation__

    def __passForward__(self,x):
        return self.activation(dot(self.weights,x) + self.biases)

    def __passAndReturn(self,x):
        linear = dot(self.weights,x)+self.biases
        return [linear,self.activation(linear)]

    def getWeights(self):
        return self.weights
    def getBiases(self):
        return self.biases

    def __repr__(self):
        string = '\nWeights:\n'+str(self.weights)+"\nBiases:\n"+str(self.biases)+"\n"
        return string

    def update(self,lr,deltaWeight=0,deltaBias=0,error=1):
        self.weights -= deltaWeight*lr
        self.biases -= deltaBias*lr

class Flatten(Full):
    def __init__(self,*args,input_shape=None,activation=Linear):
        if input_shape:
            super().__init__(prod(input_shape),activation=activation)
        elif len(args)>1:
            raise Exception("Too much arguments")
        else:
            super().__init__(args[0],activation=activation)

    def __call__(self,x,returnValues=False):
        if not returnValues:
            return self.__passForward__(x)
        return self.__passAndReturn(x)


    def __passForward__(self,x):
        flatten = array(x).flatten()
        return self.activation(dot(self.weights,flatten) + self.biases)

    def __passAndReturn(self,x):
        flatten = array(x).flatten()
        linear = dot(self.weights,flatten)+self.biases
        return [linear,self.activation(linear)]
