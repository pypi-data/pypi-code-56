from numpy import *
from .optimizer import Optimizer
from abc import *
import pprint
# from ..layers.layers import Full
pp = pprint.PrettyPrinter(indent=4)
class SGD(Optimizer):
    @staticmethod
    def __meanDeltas(deltas):
        deltaW,deltaB = deltas[0]
        for DW,DB in deltas[1:]:
            for i in range(len(DW)):
                deltaW[i] += DW[i]
                deltaB[i] += DB[i]
        deltaW,deltaB = array(deltaW)/len(deltas) ,array(deltaB)/len(deltas)
        return [deltaW,deltaB]

    @staticmethod
    def __calculateGradient(valuesA,valuesR,expected,loss,layers,lr):
        """
        Calculating the gradient for one batch

        params:
            valuesA- activation( WX+B ) - values after activation
            valuesR- WX+B - raw values
            expected- the expected output
            loss- the loss function
            layers- the models layers
            lr- learning rate
        return:
            (deltaWeights, deltaBiases)- for one batch
        """

        activationGradient = layers[-1].activation(valuesA[-1],back=True) if layers[-1].__withActivation__ else layers[-1].activation(valuesR[-1],back=True)
        delta = loss(valuesA[-1],expected,gradient=True)*activationGradient
        deltaW = outer(valuesA[-2],delta)
        weightDeltas = [transpose(deltaW)]
        biasDeltas = [array(*[delta])]
        for i,layer in enumerate(reversed(layers[:-1])):
            activationGradient = layer.activation(valuesA[-i-2],back=True) if layer.__withActivation__ else layer.activation(valuesR[-i-2],back=True)
            delta = dot(transpose(layers[-1-i].getWeights()),delta)*activationGradient
            deltaW = outer(transpose(valuesA[-i-3]),delta)
            weightDeltas.append(transpose(deltaW))
            biasDeltas.append(delta)

        return [weightDeltas,biasDeltas]

    @staticmethod
    def getGradiants(values,expected,loss,layers,lr):
        deltas = []
        for batch in range(len(values)):
            valuesA,valuesR = values[batch][0],values[batch][1]
            deltas.append(SGD.__calculateGradient(valuesA,valuesR,expected[batch],loss,layers,lr))

        return SGD.__meanDeltas(deltas)

    def __call__(self,values,expected,loss,layers,lr=0.01):
        return self.getGradiants(values,expected,loss,layers,lr)
