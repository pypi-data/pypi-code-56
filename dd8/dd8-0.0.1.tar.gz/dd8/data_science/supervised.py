# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 09:28:08 2019

@author: LIM YUAN QING
"""

import enum
import numpy as np
import pandas as pd


import sklearn.naive_bayes as nb
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

from .. import modUtils3 as utils
from dd_package.data_science.modDSEnums3 import *

logger = utils.get_basic_logger(__name__, utils.logging.DEBUG)

## Steps in using Scikit-Learn estimator API
## 1. Choose a class of model by importing the appropriate estimator class from
##    Scikit-Learn
## 2. Choose model hyperparameters by instantiating the class with desired values
## 3. Arrange data into a features matrix and target vector
## 4. Fit the model to data by calling the fit() method of the model instance
## 5. Apply the model to new data
##    a. for supervised learning, often predict lanels for unknown data using
##       the predict() method
##    b. for unsupervised learning, often transform or infer properties of the
##       data using the transform() or predict() method

## According to mind map provided by Scikit-Learn:
## 1. Classification (>50 samples && categorical target && supervised)
##    a. Linear Support Vector Classifier (<100,000 samples)
##    b. Naive Bayes
##    c. K Nearest Neighbours Classifier
##    d. Support Vector Classifier
##    e. Stochastic Gradient Descent Classifier
##    f. Kernel Approximation
##    g. Ensemble Classifiers
## 2. Clustering
## 3. Regression
## 4. Dimensionality Reduction

class LinearModels(object):
    def __init__(self, model):
        self.model = model
        
    
        

class Bayes():
    """
    Module contains implementation of Bayesian methods. Bayesian methods are eager
    learners. Eager learners immediately analyse the training data and build a model
    which is then used to classify any new data instance. Lazy learners need to go
    through the entire training dataset to calssify a new data instance (e.g. Nearest
    Neighbour).
    
    Assumptions
    -----------
    All features are conditionally independent
        p(X, y) = p(X|y)p(y)
        p(X|y) = p(x1|y) * p(x2|y) * ... * p(xN|y)
    
    Methods
    -------
    Gaussian
    Multinomial
    Complement
    Bernoulli 
    
    """
    def __init__(self, 
                 obj_data_preparation,                 
                 enum_method=ENUM_BAYESIAN_METHOD.GAUSSIAN,
                 bln_laplacian_correction=False,
                 **kwargs):
        self.__enum_method = enum_method
        self.__obj_data_preparation = obj_data_preparation
        lst_train_test_split = self.__obj_data_preparation.get_train_test_split(bln_as_np_array=True)
        lst_train_test_split = [arr.ravel() if arr.shape[1]==1 else arr 
                                for arr in lst_train_test_split ]        
        if enum_method == ENUM_BAYESIAN_METHOD.GAUSSIAN:
            self.__model = nb.GaussianNB(**kwargs)   
        elif enum_method == ENUM_BAYESIAN_METHOD.MULTINOMIAL:
            self.__model = nb.MultinomialNB(**kwargs)
        elif enum_method == ENUM_BAYESIAN_METHOD.COMPLEMENT:
            self.__model = nb.ComplementNB(**kwargs)
        elif enum_method == ENUM_BAYESIAN_METHOD.BERNOULLI:
            self.__model = nb.BernoulliNB(**kwargs)
        else:
            logger.debug('Model not supported.')
            
        self.__model.fit(lst_train_test_split[0], lst_train_test_split[2])
        self.__score = (self.__model.score(lst_train_test_split[0], lst_train_test_split[2]),
                        self.__model.score(lst_train_test_split[1], lst_train_test_split[3]))
            
    def get_model(self):
        return self.__model
    
    def get_classes(self):
        return self.__model.classes_
    
    def predict(self, df_X):
        if type(df_X) is list:
            __ = np.asarray(df_X)
        elif type(df_X) is np.ndarray:
            __ = df_X
        elif type(df_X) is pd.DataFrame:
            __ = df_X.values
        else:
            logger.debug('Unsupported data type for `df_X`.')
        
        return self.__model.predict(__)
    
    def get_score(self):
        return self.__score
    
    def get_report(self):
        return classification_report()
    
    def get_cross_val_score(self):
        x = np.concatenate((self.__lst_train_test_split[0],self.__lst_train_test_split[1]),axis=0)
        y = np.concatenate((self.__lst_train_test_split[2],self.__lst_train_test_split[3]),axis=0)
        print(x.shape)
        print(y.shape)
        return cross_val_score(self.__model, 
                               x,
                               y,
                               cv=10)