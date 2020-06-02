#اللهِ الرَّحْمٰنِ الرَّحِيمِ(Bismillahirrahmanirrahim)
#-- Vega 0.1 (Neural Network Library)--
# Author      : Umit Aksoylu
# Date        : 26.05.2020
# Description : Neural Network Library From Scratch
# Website     : http://umit.space
# Mail        : umit@aksoylu.space
# Github      : https://github.com/Aksoylu/Vega

import numpy as np
import array as arr 
import json
import atexit
import os.path
from os import path
import datetime


class Noron:    

    def setBias(self,b):
        self.bias = b

    def setWeight(self,w):
        self.weights = w

    def __init__(self , weights , bias):
        self.weights  = weights
        self.bias     = bias

    def activationSigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def inverseSigmoid(self,x):
        sig    = self.activationSigmoid(x)
        return sig * (1 - sig)

    def feedSum(self,datas):
        t0talCalc = 0
        for weight in self.weights:
            for data in datas:
                t0talCalc +=  data * weight

        return (t0talCalc + self.bias)

    def feedforward(self,datas):
        t0tal =self.feedSum(datas)
        return self.activationSigmoid(t0tal)


class Katman:

    def randomWeight(self,size):
        weights=[]
        for i in range(size):
            weights.append(np.random.normal())
        return weights

    def randomBias(self):
        return np.random.normal()

    def activationSigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def inverseSigmoid(self,x):
        sig    = self.activationSigmoid(x)
        return sig * (1 - sig)

    def backPropogation(self,dLoss_dPrediction, learning_rate,x):
        # Aynı zamanda tahmin değerinin H1 ve H2'ye göre türevlerinin de
        # hesaplanması gerekmektedir. 

        size = len(self.neurons)
        for i in range(size):
            #O ,yani  next (output) layeri 
            neuron_prediction = self.O_1.weights[0] * self.inverseSigmoid(self.neurons[i].feedSum(x))
            #tum agirliklari guncelle
            t = 0
            for weight in self.neurons[i].weights:
                #print("=======")
                #print(t)
                d_neuron_w = x[i] * self.inverseSigmoid(self.neurons[i].feedSum(x))
                self.neurons[i].weights[t] = self.neurons[i].weights[t] - (learning_rate * dLoss_dPrediction * neuron_prediction * d_neuron_w)
                t = t + 1

            #bu noron icin bias degerini guncelle

            d_neuron_b =  self.inverseSigmoid(self.neurons[i].feedSum(x))
            self.neurons[i].bias = self.neurons[i].bias - (learning_rate * dLoss_dPrediction * neuron_prediction * self.neurons[i].bias)

            weightCount = len(self.O_1.weights)
            for c in range(weightCount):
                d_out_w = self.activationSigmoid(self.neurons[i].feedSum(x))
                d_out_prediction =  d_out_w * self.inverseSigmoid(self.O_1.feedSum(x))
                self.O_1.weights[c] = self.O_1.weights[c] - (learning_rate * dLoss_dPrediction * d_out_prediction) 
                c = c + 1


        # Out nöronu için bias guncelleme
        d_out_bias = self.inverseSigmoid(self.O_1.feedSum(x))
        self.O_1.bias = self.O_1.bias - (learning_rate * dLoss_dPrediction * d_out_bias)
        ########################################################################################################################

    def saveLock(self,value):
        if value==True:
            atexit.register(exit_handler,self)
        else:
            atexit.unregister(exit_handler)

    def setEpochLock(self,value):
        if value != 0:
            self.epochLock = value

    def __init__(self, noronList,WeightList):

        self.neurons = []
        self.name = ""
        self.epochLock = 0
        for x, y in zip(noronList , WeightList):
            for i in range(x):
                self.neurons.append ( Noron(self.randomWeight(y), self.randomBias()))

        for n in self.neurons:
            print(n)

        print("Active Neurons:",len(self.neurons))
        print("---------")
        self.O_1 =  Noron(self.randomWeight(y), self.randomBias())

    def feedforward(self,data):


        processedCollection = []
        size = len(self.neurons)
        for i in range(size):
            processed = self.neurons[i].feedforward(data)
            processedCollection.append(processed)

        NetworkOut = self.O_1.feedforward(processedCollection)
        #L1_1_processed = self.L1_1.feedforward(data)
        #L1_2_processed = self.L1_2.feedforward(data)
        #NetworkOut = self.O_1.feedforward([L1_1_processed,L1_2_processed])
        return NetworkOut

    # Kısmı türev çok değişkenli bir fonksiyonda bir değişkenin o fonskiyonu
    # ne kadar etkilediğini elde etmek için kullanılmaktadır.

    def mse_loss(self , y_real , y_prediction):
        # y_real ve y_prediction aynı boyutta numpy arrayleri olmalıdır. 
        return ((y_real - y_prediction) ** 2).mean()

    def train(self,data,labels,learning_rate,epoch):

        for i in range(epoch):
            if i == self.epochLock and self.epochLock != 0:
                if self.name == "":
                    self.name = str(datetime.datetime.now())
                saveModel(self.name)
            for x, y in zip(data , labels):

                prediction = self.feedforward(x)
                dLoss_dPrediction = -2*(y - prediction)
                self.backPropogation(dLoss_dPrediction, learning_rate,x)

            predictions = np.apply_along_axis(self.feedforward ,1, data)
            loss = self.mse_loss(labels , predictions)
            print("Devir %d loss: %.7f" % (i, loss))

    def saveModel(self,name):
        jsonModel = {}

        jsonModel['neuron'] = {}
        index = 0
        for neuron in self.neurons:
            jsonModel['neuron'][index] = {}
            jsonModel['neuron'][index]["w"] = []
            jsonModel['neuron'][index]["b"] = ""

            weight_index = 0
            for weight in neuron.weights:
                jsonModel['neuron'][index]["w"].append(weight)
                weight_index = weight_index + 1
            jsonModel['neuron'][index]["b"] = neuron.bias

            index = index + 1

        #at least, add output neuron
        jsonModel['neuron']['OUT'] = {}
        jsonModel['neuron']['OUT']["w"] = []
        jsonModel['neuron']['OUT']["b"] = self.O_1.bias

        for weight in self.O_1.weights:
            jsonModel['neuron']['OUT']["w"].append(weight)


        json_str = json.dumps(jsonModel)
        name = name + ".neurons"
        f = open(name, "w")
        f.write(json_str)
        f.close()
        #dosyaya kaydetme islemleri

    def loadModel(self,name):

        if path.exists(name) == 0 :
            print("'",name, "' Network File Is Not Found")
            return

        #dosyaya yazma islemleri
        data = ""
        with open(name, 'r') as file:
            data = file.read().replace('\n', '')

        y = json.loads(data)

        neurons = y['neuron']

        #clear old network layers in memory
        self.neurons.clear()

        for neuron in neurons:
            #set weights
            tmp_w = []
            for p in y['neuron'][neuron]['w']:
                tmp_w.append(p)

            #set bias
            b = y['neuron'][neuron]['b']

            #append neuron to network
            new_noron = Noron(tmp_w,b)
            self.neurons.append(new_noron)

        #at least, load Output neuron
        self.O_1.bias = y['neuron']['OUT']['b']
        self.O_1.weights = y['neuron']['OUT']['w']

    def displayNetwork():
        print("todo :")

def exit_handler(sel):
    Katman.saveModel(sel,sel.name)







