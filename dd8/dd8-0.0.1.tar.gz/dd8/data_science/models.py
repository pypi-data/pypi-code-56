# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:53:40 2019

@author: LIM YUAN QING

Module contains classes and functions that would 
1. convert raw data of different formats to memory-optimized pandas Dataframes
2. perform train-evaluation-test split
3. perform missing data imputation if required to
4. perform data transformation if required to
    a. binning
    b. normalization
    c. log transformation
    d. one-hot encoding

Steps in using Scikit-Learn estimator API
    1. Choose a class of model by importing the appropriate estimator class from
       Scikit-Learn
    2. Choose model hyperparameters by instantiating the class with desired values
    3. Arrange data into a features matrix and target vector
    4. Fit the model to data by calling the fit() method of the model instance
    5. Apply the model to new data
       a. for supervised learning, often predict lanels for unknown data using
          the predict() method
       b. for unsupervised learning, often transform or infer properties of the
          data using the transform() or predict() method

According to mind map provided by Scikit-Learn:
    1. Classification (>50 samples && categorical target && supervised)
       a. Linear Support Vector Classifier (<100,000 samples)
       b. Naive Bayes
       c. K Nearest Neighbours Classifier
       d. Support Vector Classifier
       e. Stochastic Gradient Descent Classifier
       f. Kernel Approximation
       g. Ensemble Classifiers
    2. Clustering
    3. Regression
    4. Dimensionality Reduction

Optimization
    Fix random state for all models

    1. Random Forrest
       a. criterion (gini, entropy)
       b. n_estimators (np.arange(100, 500, 100))

Classes
-------
DataPreparation(X, y, data_type=ENUM_DATA_SET_TYPE.CROSS_SECTIONAL)

ENUM_DATA_SET_TYPE

ENUM_DATA_TYPE

"""

import sklearn.utils.testing
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report

from .modDataPreparation3 import Data
from .modDSEnums3 import ENUM_MACHINE_LEARNING_TYPE, ENUM_DATA_SET_TYPE, \
                            ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS, \
                            ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS, \
                            ENUM_CROSS_SECTIONAL_REGRESSION_MODELS, \
                            ENUM_DATA_TYPE
from .modDSGlobal3 import DIC_DEFAULT_PARAM_GRIDS, DIC_GRID_SEARCH_DEFAULT_PARAM_GRIDS, \
                            DIC_GRID_SEARCH_DEFAULT_SCORER, DIC_SKLEARN_ESTIMATORS
from ..modUtils3 import get_basic_logger
from ..modGlobal3 import LOG_PRINT_LEVEL, LOG_WRITE_LEVEL


logger = get_basic_logger(__name__, LOG_PRINT_LEVEL)

class DataTransformer(object):
    def __init__(self, enum_model = ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.LINEAR):
        self.__dic_transformations = dict()
        self.enum_model = enum_model
        
      
        
    def fit(self, X, y = None):
        if (isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS) or
            isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS) or 
            isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_REGRESSION_MODELS)):
            data = Data(X, y, ENUM_DATA_SET_TYPE.CROSS_SECTIONAL)
            features_dtype = data.features_data_type_enums
            features_descriptive = data.get_features_descriptive_statistics()
            if isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS):
                if self.enum_model is ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS.GAUSSIAN_NIAVE_BAYES:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS.LOGISTIC:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS.RANDOM_FOREST:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS.KNN:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS.SGD:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS.SVM:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS.MLP:
                    pass
                else:
                    logger.error('`ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS` not supported!')
            elif isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS):
                if self.enum_model is ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS.K_MEANS:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS.SPECTRAL:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS.HIERARCHICAL:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS.DBSCAN:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS.BIRCH:
                    pass
                else:
                    logger.error('`ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS` not supported!')
            elif isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_REGRESSION_MODELS):
                if self.enum_model is ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.LINEAR:
                    ## 1. normalise
                    ## 2. pca
                    numeric_data = data.get_features_descriptive_statistics()[ENUM_DATA_TYPE.NUMERIC]
                    for col in numeric_data.columns:
                        col_stats = numeric_data[col]
                        print(col_stats)
                        #self.__lst_transformations.append((col, transformer))
                elif self.enum_model is ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.SGD:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.LASSO:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.ELASTIC_NET:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.SUPPORT_VECTOR:
                    pass
                elif self.enum_model is ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.RIDGE:
                    pass
                else:
                    logger.error('`ENUM_CROSS_SECTIONAL_REGRESSION_MODELS` not supported!')
            else:
                logger.error('`enum_model` not supported!')
        

class GridSearchCustom(object):
    def __init__(self, X_train, X_test, y_train=None, y_test=None, 
                 enum_machine_learning_type = ENUM_MACHINE_LEARNING_TYPE.CLASSIFICATION,                 
                 dic_potential_estimators = None,
                 dic_transformations = None,
                 dic_param_grids = None):        
        
        self.features_train = X_train
        self.features_test = X_test
        self.targets_train = y_train
        self.targets_test = y_test
        
        self.enum_machine_learning_type = enum_machine_learning_type
        
        self.transformations = dic_transformations
        self.potential_estimators = dic_potential_estimators
        self.param_grids = dic_param_grids
        
    def fit(self):
        # for each estimator
        # 1. no data transformation
        #    - loop through param_grid
        # 2. data transformation
        #    - loop through param_grid
        
        # transformations can apply to
        # i. column name (str)
        # ii. data type (enum)
        # iii. whole dataset, column-wise (str:column-wise)
        # iv. entire dataset (str:entire)
        for name, estimator in self.potential_estimators.items():
            if name == 'LinearRegression':
                pass
            
            for transformation in self.transformations[name]:
                pass
                
        
        grid = GridSearchCV(estimator(), param_grid, cv=self.__cross_validator)
        grid.fit(self.features, self.targets)   
        self.__dic_lst_grid_searches[name].append(grid)
        
class ParamGridSelector(object):
    def __init__(self, 
                 X,
                 y = None,
                 enum_model = ENUM_CROSS_SECTIONAL_REGRESSION_MODELS.LINEAR):
        self.features = X
        self.targets = y
        self.enum_model = enum_model
        
    def get_param_grid(self):
        
        if isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS):
            pass
        elif isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS):
            pass
        elif isinstance(self.enum_model, ENUM_CROSS_SECTIONAL_REGRESSION_MODELS):
            pass
        else:
            logger.error('`enum_model` not implemented!')
                 


class ModelSelector(object):
    dic_sklearn_estimators = DIC_SKLEARN_ESTIMATORS
    def __init__(self, X, 
                 y = None,
                 enum_machine_learning_type=ENUM_MACHINE_LEARNING_TYPE.CLASSIFICATION,
                 enum_data_set_type=ENUM_DATA_SET_TYPE.CROSS_SECTIONAL):

        self.__dic_potential_estimators = dict()
        self.features = X
        self.targets = y
        
        ## TO IMPLEMENT: DETERMINE MODELS BASED ON DATASET CHARACTERISTICS ##
        ## THIS IS THE REASON FOR PASSING X and y INTO THIS CLASS!!        ##
        
        if (enum_machine_learning_type is ENUM_MACHINE_LEARNING_TYPE.CLASSIFICATION and
            enum_data_set_type is ENUM_DATA_SET_TYPE.CROSS_SECTIONAL):
            for model in ENUM_CROSS_SECTIONAL_CLASSIFICATION_MODELS:
                self.add_estimator(model.value)
        elif (enum_machine_learning_type is ENUM_MACHINE_LEARNING_TYPE.CLUSTERING and
            enum_data_set_type is ENUM_DATA_SET_TYPE.CROSS_SECTIONAL):
            for model in ENUM_CROSS_SECTIONAL_CLUSTERING_MODELS:
                self.add_estimator(model.value)        
        elif (enum_machine_learning_type is ENUM_MACHINE_LEARNING_TYPE.REGRESSION and
            enum_data_set_type is ENUM_DATA_SET_TYPE.CROSS_SECTIONAL):
            for model in ENUM_CROSS_SECTIONAL_REGRESSION_MODELS:
                self.add_estimator(model.value)  
        
    def get_potential_estimators(self):
        return self.__dic_potential_estimators
    
    def add_estimator(self, str_estimator_name):
        if str_estimator_name in ModelSelector.dic_sklearn_estimators:
            self.__dic_potential_estimators[str_estimator_name] = ModelSelector.dic_sklearn_estimators[str_estimator_name]
        else:
            logger.warning('{estimator_name} does not exist in sklearn!'.format(estimator_name=str_estimator_name))       
        
        return self.__dic_potential_estimators
    
    def remove_estimator(self, str_estimator_name):
        return self.__dic_potential_estimators.pop(str_estimator_name, None)
    
    
class ModelOptimizer(object):
    def __init__(self, X, 
                 y=None, 
                 dic_potential_estimators=None,
                 dic_lst_param_grids = None,
                 dic_lst_scorer = None,
                 cross_validator=None,
                 bln_tune = False):
        self.features = X
        self.targets = y
        self.__dic_potential_estimators = dic_potential_estimators
        if cross_validator:
            self.__cross_validator = cross_validator
        else:
            self.__cross_validator = 5
#        self.__cross_validator = cross_validator      
        self.__dic_lst_grid_searches = dict()   
        self.__dic_lst_scorer = dict()
        self.__bln_tune = bln_tune
        if dic_lst_scorer:
            if isinstance(dic_lst_scorer, dict):
                self.__dic_lst_scorer = dic_lst_scorer
            else:
                logger.error('missing scorer function in the following format: {estimator_name: [list of scorer names]}')
        else: 
            self.__dic_lst_scorer = DIC_GRID_SEARCH_DEFAULT_SCORER
            
        if self.__bln_tune:
            if dic_lst_param_grids:
                if isinstance(dic_lst_param_grids, dict):
                    self.__dic_lst_param_grids = dic_lst_param_grids
                else:
                    logger.error('`dic_lst_param_grids` must be a dictionary of list of dictionaries \
                                in the following format: {estimator_name: [{set_1_param_name: [val1, val2, ...]}, \
                                {set_2_param_name: [val1, val2, ...]}]')
            else:
                self.__dic_lst_param_grids = DIC_GRID_SEARCH_DEFAULT_PARAM_GRIDS                
        else:
            self.__dic_lst_param_grids = DIC_DEFAULT_PARAM_GRIDS   
        
    def optimize(self):
        for name, estimator in self.__dic_potential_estimators.items():            
            param_grid = dict()
            if self.__bln_tune:
                self.__dic_lst_grid_searches[name] = []
                for param_grid in self.__dic_lst_param_grids[name]:
                    
#                if name == 'GaussianNB':
#                    param_grid = {}
#                elif name == 'LogisticRegression':                    
#                    param_grid = {'solver':['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}
#                elif name == 'RandomForestClassifier':
#                    param_grid = {'criterion':['gini','entropy']}
#                elif name == 'KNeighborsClassifier':
#                    param_grid = {}
#                elif name == 'SGDClassifier':
#                    param_grid = {}
                    
                    if name in self.__dic_lst_scorer:
                        for scorer in self.__dic_lst_scorer[name]:
                            grid = GridSearchCV(estimator(), param_grid, cv=self.__cross_validator, scoring=scorer)
                            grid.fit(self.features, self.targets)   
                            self.__dic_lst_grid_searches[name].append(grid)
                    else:
                        grid = GridSearchCV(estimator(), param_grid, cv=self.__cross_validator)
                        grid.fit(self.features, self.targets)   
                        self.__dic_lst_grid_searches[name].append(grid)
                
#        for name, lst_grid in self.__dic_lst_grid_searches.items():
#            for grid in lst_grid:
#                print(name)
#                print(grid.best_params_)
#                print(classification_report(self.targets, grid.predict(self.features)))
    
    def report(self):
        b = classification_report(data_prep.targets, grids['GaussianNB'].predict(data_prep.features))
            
            
            
    def get_grids(self):
        return self.__dic_lst_grid_searches
    
    def add_estimator(self, name, estimator, param_grid):
        self.__dic_potential_estimators[name] = estimator
        return self.__dic_potential_estimators

    def report(self):
        pass