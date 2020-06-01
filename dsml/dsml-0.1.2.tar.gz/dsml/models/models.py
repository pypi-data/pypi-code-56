import numpy as np
from .model import Model

class Sequential(Model):
    def __init__(self,*args):
        self.firstActivation = args[0].activation

        self.layers = [*args][:-1]
        for i,layer in enumerate(args[:-1]):
            self.layers[i].init(args[i+1].inAmount,args[i+1].activation)

    def make(self,optimizer=None,loss=None,lr=0.01):
        self.optimizer = optimizer()
        self.loss = loss()
        self.lr = lr

    def __feedforward(self,x,train=False):
        #Activation and raw values
        valuesA = [x]
        valuesR = [x]
        x = self.firstActivation(np.array(x))

        if train:
            x = self.layers[0](x,returnValues=True)
            valuesR.append(x[0])
            valuesA.append(x[1])
            for layer in self.layers[1:]:#To get the Raw and activated outputs
                x = layer(x[1],returnValues=True)
                valuesR.append(x[0])
                valuesA.append(x[1])
            return [valuesA,valuesR]

        else:
            for layer in self.layers:
                x = layer(x)

        return x

    def predict(self,x,getValues=False):
        values = []
        for i,sample in enumerate(x):
            values.append(self.__feedforward(sample,train=getValues))
        return values


    def train(self,x,y,epochs=1,batch_size=1):
        for i in range(epochs):
            error = self.loss(self.predict(x),y)
            print(error)

            randomState = np.random.get_state()
            np.random.shuffle(x)
            np.random.set_state(randomState)
            np.random.shuffle(y)

            for j,batch in enumerate(zip(np.array_split(x,batch_size),np.array_split(y,batch_size))):
                batchX,batchY = batch
                values = self.predict(batchX,getValues=True)
                weightDeltas, biasDeltas = self.optimizer(values,batchY,self.loss,self.layers,self.lr)

                error = self.loss(x,self.predict(x))
                for l,layer in enumerate(reversed(self.layers)):
                    layer.update(self.lr,deltaWeight=weightDeltas[l],deltaBias=biasDeltas[l],error=error)
