# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 07:13:37 2019

@author: yuanq
"""

from sklearn.metrics import make_scorer, silhouette_score
from sklearn.utils.testing import all_estimators
from sklearn.decomposition import PCA

import numpy as np
RANDOM_STATE = np.random.RandomState(seed=1)
#RANDOM_STATE = None

DIC_SKLEARN_ESTIMATORS = {tup[0]:tup[1] for tup in all_estimators()}

DIC_DEFAULT_PARAM_GRIDS = {'RandomForestClassifier': {'random_state':RANDOM_STATE},
                           'SGDClassifier': {'random_state':RANDOM_STATE},                           
                           'Lasso': {'random_state':RANDOM_STATE},
                           'SGDRegressor': {'random_state':RANDOM_STATE},
                           'Ridge': {'random_state':RANDOM_STATE}}  

DIC_GRID_SEARCH_DEFAULT_PARAM_GRIDS = {'GaussianNB': [{'priors':[None],
                                                       'var_smoothing':[1e-09]}],
                                      'LogisticRegression': [{'solver':['newton-cg', 'lbfgs', 'sag'],
                                                                'penalty':['l2','none'],                                                            
                                                                'multi_class':['auto'],
                                                                'max_iter':[5000],
                                                                'random_state':[RANDOM_STATE]},
                                                             {'solver':['saga'],
                                                                'penalty':['l1','l2','none'],
                                                                'multi_class':['auto'],
                                                                'max_iter':[5000],
                                                                'random_state':[RANDOM_STATE]},
                                                             {'solver':['saga'],
                                                                'penalty':['elasticnet'],
                                                                'multi_class':['auto'],
                                                                'max_iter':[5000],
                                                                'l1_ratio':[0.2,0.4,0.6,0.8],
                                                                'random_state':[RANDOM_STATE]},
                                                             {'solver':['liblinear'],
                                                                'penalty':['l1','l2'],
                                                                'multi_class':['auto'],
                                                                'max_iter':[5000],
                                                                'random_state':[RANDOM_STATE]},],
                                      'RandomForestClassifier': [{'n_estimators':[10,50,100,150,200],
                                                                  'criterion':['gini','entropy'],
                                                                  'random_state':[RANDOM_STATE]}],
                                      'KNeighborsClassifier': [{'n_neighbors':[5,10,15,20,25,30],
                                                                'weights':['uniform','distance'],
                                                                'algorithm':['auto'],
                                                                'p':[1,2]}],
                                      'SGDClassifier': [{'loss':['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'],
                                                         'penalty':['l2', 'l1', 'elasticnet', 'none'],
                                                         'alpha':[0.0001, 0.001],
                                                         'l1_ratio':[0.2,0.4,0.6,0.8],
                                                         'max_iter':[5000],
                                                         'random_state':[RANDOM_STATE]}],
                                                              
#                                    'MLPClassifier': [{'hidden_layer_sizes': (100, ), activation=’relu’, solver=’adam’, alpha=0.0001, batch_size=’auto’, learning_rate=’constant’, learning_rate_init=0.001, power_t=0.5, max_iter=200, shuffle=True, random_state=None, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10)[source]
                                      
                                      'LinearRegression': [{'fit_intercept':[True, False] ,
                                                            'normalize':[True, False],
                                                            'random_state':[RANDOM_STATE]}],
                                      'Lasso': [{'alpha': [1.0],
                                                 'fit_intercept':[True, False] ,
                                                 'max_iter':[5000],
                                                 'normalize':[True, False],
                                                 'random_state':[RANDOM_STATE]}],
                                      'SGDRegressor': [{'loss':['squared_loss','huber','epsilon_insensitive',
                                                                'squared_epsilon_insensitive'],
                                      'penalty':['l2','l1','elasticnet'], 
                                      'alpha':[0.0001], 
                                      'l1_ratio':[0.15], 
                                      'fit_intercept':[True, False],
                                      'max_iter':[1000], 
                                      'epsilon':[0.1], 
                                      'learning_rate':['invscaling','constant','adaptive','optimal'],
                                      'random_state':[RANDOM_STATE]}],
                                      'ElasticNet': [{'alpha': [1.0],
                                                      'ratio': np.arange(0,1,0.1),
                                                 'fit_intercept':[True, False] ,
                                                 'max_iter':[5000],
                                                 'normalize':[True, False],
                                                 'random_state':[RANDOM_STATE]}],
                                      'SVR': [{'kernel': ['linear','poly','rbf','sigmoid','precomputed'],
                                               'degree':[3],
                                               'C': [1.0],
                                               'epsilon':[0.1],
                                                 'shrinking':[True, False] ,
                                                 'max_iter':[5000],
                                                 'normalize':[True, False]}],
                                      'Ridge': [{'alpha':[1.0],
                                                 'max_iter':[1],
                                                 'solver': ['auto','svd','cholesky','lsqr','sparse_cg','sag','saga'],
                                                            'normalize':[True, False],
                                                            'random_state':[RANDOM_STATE]}],
                                    'KMeans': [{'n_clusters': np.arange(2,10,1),
                                                            'random_state':[RANDOM_STATE]}]
#                                    'AgglomerativeClustering': [],
#                                    'SpectralClustering': [],
#                                    'Birch': [],
#                                    'DBSACN': []
}
                                      
DIC_GRID_SEARCH_DEFAULT_SCORER = {'KMeans': [make_scorer(silhouette_score,greater_is_better=True)]}                    