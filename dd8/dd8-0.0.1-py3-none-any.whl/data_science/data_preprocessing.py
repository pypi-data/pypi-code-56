# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 14:19:42 2018

@author: LIM YUAN QING

Module contains classes and functions that would 
1. convert raw data of different formats to memory-optimized pandas Dataframes
2. determine treatment for missing data
2. perform train-test split / create cross-validator object
3. perform missing data imputation if required to
4. perform data transformation if required to
    a. binning
    b. normalization
    c. log transformation
    d. one-hot encoding


Classes
-------
DataPreparation(X, y, data_type=ENUM_DATA_SET_TYPE.CROSS_SECTIONAL)
1. profile data
2. profile missing data


ENUM_DATA_SET_TYPE

ENUM_DATA_TYPE

"""
# Road map
# --------
# 1. Determine if variables are of numeric or non-numeric types
# 2. For numeric data types, determine if variable is categorical or continuous
# 3. Descriptive statistics
# 4. Optimise memory usage

import pandas as pd
from sklearn.model_selection import KFold, RepeatedKFold, LeaveOneOut, LeavePOut, \
                                    ShuffleSplit, StratifiedKFold, StratifiedShuffleSplit                                    
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt

from dd8 import LOG_PRINT_LEVEL, LOG_WRITE_LEVEL
from dd8.data_science.enums import ENUM_DATA_SET_TYPE, ENUM_CROSS_VALIDATION_METHOD, ENUM_DATA_TYPE
from dd8.data_science.stats import DescriptiveStatistics, get_best_fit_distribution
from dd8.utility.panda_utils import optimize_mem_usage
from dd8.utility.utils import get_basic_logger, get_dataframe_info, conditional_decorator, dec_calculate_time

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

"""
Revamp

1. cross_validator
2. loop through each cross validator
3. perform data transformation (until 1 step before estimator)
4. gridsearch model parameters
5. next loop for cross validator



"""
class Data(object):
    def __init__(self):
        pass
    
class TimeSeriesData():
    def __init__(self, X,
                 y=None,
                 enum_data_set_type=ENUM_DATA_SET_TYPE.TIME_SERIES):
        pass

class CrossSectionalData(Data):
    '''
    Data object with memory-optimized pandas DataFrame containing features and 
    targets of a dataset.
    
    Parameters
    ----------
    X : pandas DataFrame object
        features dataset
    y : pandas DataFrame object, optional
        targets dataset (default is None)
    enum_data_set_type : ENUM_DATA_SET_TYPE 
                            ENUM_DATA_SET_TYPE.CROSS_SECTIONAL
                            ENUM_DATA_SET_TYPE.TIME_SERIES
                            ENUM_DATA_SET_TYPE.TEXT
                            ENUM_DATA_SET_TYPE.IMAGE
                            ENUM_DATA_SET_TYPE.VIDEO
                            ENUM_DATA_SET_TYPE.AUDIO
    '''
    
    @conditional_decorator(dec_calculate_time, IS_DEVELOPMENT)
    def __init__(self, X, 
                 y=None,
                 enum_data_set_type=ENUM_DATA_SET_TYPE.CROSS_SECTIONAL):
        
        ## instantiating object attributes
        logger.debug('instantiating `Data` object...')
        assert isinstance(X, pd.DataFrame), "X is not a pandas DataFrame"
        if not y is None:
            assert isinstance(y, pd.DataFrame), "y is not a pandas DataFrame"
            assert X.shape[0] == y.shape[0], "X and y have different number of rows"             
        self.__lst_derived_features = []
        self.__dic_distributions = dict()
        self.enum_data_set_type = enum_data_set_type        
        self.features_to_sample_size_ratio = None
        
        self.features_shape = None
        self.features_names = None
        self.features_info = None
        self.__dic_features_descriptive_statistics = dict()
        self.features_data_type_enums = dict()
        self.features_by_data_type_enums = dict()
        
        self.targets_shape = None
        self.targets_names = None
        self.targets_info = None
        self.__dic_targets_descriptive_statistics = dict()        
        self.targets_data_type_enums = dict()        
        self.targets_by_data_type_enums = dict()
        
        self.features = X.copy()
        logger.debug('optimizing features dataframe...')
        for var in self.features.columns:
            self.features[var] = optimize_mem_usage(self.features[var]) 
        
        logger.debug('describing features...')
        self.features_shape = self.features.shape
        self.features_to_sample_size_ratio = self.features_shape[1]/self.features_shape[0]
        if self.features_to_sample_size_ratio >= 1.0:
            logger.warning('potential overfitting - there are {n_features} features but only \
                           {n_rows} data points...'.format(n_features=self.features_shape[1],
                           n_rows=self.sample_size))
        self.features_names = tuple(self.features.columns)
        self.features_info = get_dataframe_info(self.features)   
        
        self.features_data_type_enums = {var:get_data_type_enum(self.features[var])
                                            for var in self.features.columns}        
        for var in self.features.columns:            
            if self.features_data_type_enums[var] in self.__dic_features_descriptive_statistics:
                self.__dic_features_descriptive_statistics[self.features_data_type_enums[var]] =  pd.concat([self.__dic_features_descriptive_statistics[self.features_data_type_enums[var]], 
                                                 DescriptiveStatistics(self.features[var],self.enum_data_set_type, self.features_data_type_enums[var]).summary],axis=1)
            else:
                self.__dic_features_descriptive_statistics[self.features_data_type_enums[var]] = DescriptiveStatistics(self.features[var],self.enum_data_set_type, self.features_data_type_enums[var]).summary
                
            if self.features_data_type_enums[var] in self.features_by_data_type_enums:
                self.features_by_data_type_enums[self.features_data_type_enums[var]].append(var)
            else:
                self.features_by_data_type_enums[self.features_data_type_enums[var]] = [var]
                
 
        if not y is None:
            self.targets = y.copy()
            logger.debug('optimizing targets dataframe...')
            for var in self.targets.columns:
                self.targets[var] = optimize_mem_usage(self.targets[var])  

            logger.debug('describing targets...')
            self.targets_shape = self.targets.shape
            self.targets_names = tuple(self.targets.columns)
            self.targets_info = get_dataframe_info(self.targets)        
            
            self.targets_data_type_enums = {var:get_data_type_enum(self.targets[var])
                                                for var in self.targets.columns}
            for var in self.targets.columns:            
                if self.targets_data_type_enums[var] in self.__dic_targets_descriptive_statistics:
                    self.__dic_targets_descriptive_statistics[self.targets_data_type_enums[var]] = pd.concat([self.__dic_targets_descriptive_statistics[self.targets_data_type_enums[var]], 
                                                     DescriptiveStatistics(self.targets[var],self.enum_data_set_type, self.targets_data_type_enums[var]).summary],axis=1)
                else:
                    self.__dic_targets_descriptive_statistics[self.targets_data_type_enums[var]] = DescriptiveStatistics(self.targets[var],self.enum_data_set_type, self.targets_data_type_enums[var]).summary                
                    
                if self.targets_data_type_enums[var] in self.targets_by_data_type_enums:
                    self.targets_by_data_type_enums[self.targets_data_type_enums[var]].append(var)
                else:
                    self.targets_by_data_type_enums[self.targets_data_type_enums[var]] = [var]
        else:
            self.targets = None

    def get_numeric_features(self):
        try:
            return self.features[self.features_by_data_type_enums[ENUM_DATA_TYPE.NUMERIC]]
        except KeyError:
            return None

    def get_categorical_features(self):
        try:
            return self.features[self.features_by_data_type_enums[ENUM_DATA_TYPE.CATEGORICAL]]
        except KeyError:
            return None

    def get_textual_features(self):
        try:
            return self.features[self.features_by_data_type_enums[ENUM_DATA_TYPE.TEXTUAL]]
        except KeyError:
            return None

    def get_date_features(self):
        try:
            return self.features[self.features_by_data_type_enums[ENUM_DATA_TYPE.DATE]]
        except KeyError:
            return None
    
    def get_enum_data_set_type(self):
        return self.enum_data_set_type

    def get_features_to_sample_ratio(self):
        return self.features_to_sample_size_ratio
    
    def get_features_shape(self):
        return self.features_shape
    
    def get_targets_shape(self):
        return self.targets_shape
    
    def get_features_names(self):
        return self.features_names
    
    def get_targets_names(self):
        return self.targets_names
    
    def get_features_info(self):
        return self.features_info
    
    def get_targets_info(self):
        return self.targets_info
    
    def get_features_data_type_enums(self):
        return self.features_data_type_enums
    
    def get_targets_data_type_enums(self):
        return self.targets_data_type_enums
    
    def get_features_by_data_type_enums(self):
        return self.features_by_data_type_enums
    
    def get_targets_by_data_type_enums(self):
        return self.targets_by_data_type_enums                    
         
    def get_features_descriptive_statistics(self):
        return self.__dic_features_descriptive_statistics
        
    def get_targets_descriptive_statistics(self):
        return self.__dic_targets_descriptive_statistics  

    def set_data_type(self, str_var_name, pd_dtype, bln_from_features=True):        
        logger.debug('changing data type for {var_name} from {data_set}...').format(var_name=str_var_name,
                    data_set=(bln_from_features*'features' + (not bln_from_features*'targets')))
        if bln_from_features:            
            self.__dic_features_descriptive_statistics[self.features_data_type_enums[str_var_name]].drop([str_var_name],axis=1,inplace=True)
            self.features[str_var_name] = optimize_mem_usage(self.features[str_var_name].astype(pd_dtype))
            self.features_info.update(get_dataframe_info(pd.DataFrame(self.features[str_var_name])))
            self.features_data_type_enums[str_var_name] = get_data_type_enum(self.targets[str_var_name])
            self.__dic_features_descriptive_statistics[self.features_data_type_enums[str_var_name]] = DescriptiveStatistics(self.features[str_var_name],self.enum_data_set_type, self.features_data_type_enums[str_var_name]).summary
            return self.features_info
        else:
            self.__dic_targets_descriptive_statistics[self.targets_data_type_enums[str_var_name]].drop([str_var_name],axis=1,inplace=True)
            self.targets[str_var_name] = optimize_mem_usage(self.targets[str_var_name].astype(pd_dtype))
            self.targets_info.update(get_dataframe_info(pd.DataFrame(self.targets[str_var_name])))
            self.targets_data_type_enums[str_var_name] = get_data_type_enum(self.targets[str_var_name])
            self.__dic_targets_descriptive_statistics[self.targets_data_type_enums[str_var_name]] = DescriptiveStatistics(self.targets[str_var_name],self.enum_data_set_type, self.targets_data_type_enums[str_var_name]).summary
            return self.targets_info
    
    def drop_features(self, lst_col_names):
        
        if isinstance(lst_col_names, str):
            lst_col_names_to_drop = [lst_col_names]
        elif isinstance(lst_col_names, list):
            lst_col_names_to_drop = lst_col_names
        else:
            logger.error('`lst_col_names` must be a string or a list of strings!')
        try:
            for str_col_name in lst_col_names_to_drop:
                self.features.drop(columns=[str_col_name],inplace=True)
                self.features_info.drop([str_col_name], inplace=True)
                self.__dic_features_descriptive_statistics[self.features_data_type_enums[str_col_name]].drop(columns=[str_col_name], inplace=True)
                self.features_by_data_type_enums[self.features_data_type_enums[str_col_name]] = [var for var in self.features_by_data_type_enums[self.features_data_type_enums[str_col_name]] if var != str_col_name]            
                self.features_data_type_enums.pop(str_col_name)        
            
            self.features_shape = self.features.shape
            self.features_names = tuple(self.features.columns)
            self.__lst_derived_features = [var for var in self.__lst_derived_features if (not var in lst_col_names_to_drop) ]                
            return True
        except:
            return False
        
    def add_features(self, df_data):
        if isinstance(df_data, pd.DataFrame):
            for col in df_data.columns:
                self.features[col] = optimize_mem_usage(df_data[col])
                self.features_info.update(get_dataframe_info(pd.DataFrame(self.features[col])))
                self.features_data_type_enums[col] = get_data_type_enum(self.features[col])
                self.__dic_features_descriptive_statistics[self.features_data_type_enums[col]] =  pd.concat([self.__dic_features_descriptive_statistics[self.features_data_type_enums[col]], 
                                                     DescriptiveStatistics(self.features[col],self.enum_data_set_type, self.features_data_type_enums[col]).summary],axis=1)
                self.features_by_data_type_enums[self.features_data_type_enums[col]].append(col)        
                self.__lst_derived_features.append(col)                    
        elif isinstance(df_data, pd.Series):
            col = df_data.name
            self.features[col] = optimize_mem_usage(pd.DataFrame(df_data))
            self.features_info.update(get_dataframe_info(pd.DataFrame(self.features[col])))
            self.features_data_type_enums[col] = get_data_type_enum(self.features[col])
            self.__dic_features_descriptive_statistics[self.features_data_type_enums[col]] =  pd.concat([self.__dic_features_descriptive_statistics[self.features_data_type_enums[col]], 
                                                 DescriptiveStatistics(self.features[col],self.enum_data_set_type, self.features_data_type_enums[col]).summary],axis=1)
            self.features_by_data_type_enums[self.features_data_type_enums[col]].append(col)        
            self.__lst_derived_features.append(col) 
        else:
            logger.debug('`df_data` is neither an instance of pandas DataFrame nor Series class!')
            return False
        self.features_shape = self.features.shape
        self.features_names = tuple(self.features.columns)
        return True    
        
    def one_hot_encode_feature(self, str_col_name, lst_lst_mapping=None,
                                str_prefix=None, bln_drop_original=False,
                                bln_drop_first=False):
        if lst_lst_mapping:
            self.features[str_col_name + '_categories'] = 0.0
            self.__lst_derived_features.append(str_col_name + '_categories')
            count = 0
            for cat in lst_lst_mapping:
                self.features[str_col_name + '_categories'].where(~self.features[str_col_name].isin(cat), inplace=True, other=count)
                count += 1
            
            df_one_hot = pd.get_dummies(self.features[str_col_name + '_categories'],
                                        prefix=str_col_name + '_categories_', drop_first = bln_drop_first)
            self.add_features(df_one_hot)
            if bln_drop_original:
                self.drop_features([str_col_name + '_categories'])                
        else:
            df_one_hot = pd.get_dummies(self.features[str_col_name],
                                        prefix=str_prefix, drop_first = bln_drop_first)            
            self.add_features(df_one_hot)
        
        if bln_drop_original:
            self.drop_features(str_col_name)
                    
        return df_one_hot
                    
    def get_best_fit_distributions(self, lst_col_names=None, bln_recompute=False):
        if lst_col_names:
            if isinstance(lst_col_names, str):
                __ = [lst_col_names]
            elif isinstance(lst_col_names, list):
                __ = lst_col_names
            else:
                logger.error('`lst_col_names` must be a string or a list of strings!')
                
            for col in __:
                if col in self.features_by_data_type_enums[ENUM_DATA_TYPE.NUMERIC]:
                    if (not col in self.__dic_distributions) or bln_recompute:
                        self.__dic_distributions[col] = get_best_fit_distribution(self.features[col])
                        
                else:
                    logger.warning('{col_name} is not of numeric type - no distribution fitted!'.format(col_name=col))
        
        return self.__dic_distributions
    
    def gen_missing_data_statistics(self, threshold=0.0):
#        features_with_missing_data = (self.features_info[
#                self.features_info['missing_values_perc']>threshold].index.to_list())
#        dic_output= dict()   
#        pool = mp.Pool(processes = mp.cpu_count()-1)        
#        for feature in features_with_missing_data:
#            print(feature)
#            results_missing = [pool.apply(describe, args=(self.features[pd.isnull(self.features[feature])][var],), 
#                                          kwds={'nan_policy':'omit','name':var+'_missing'})
#                                for var in self.features.columns.drop(feature)
#                                if pd.api.types.is_numeric_dtype(self.features[var].dtype)]
#            results = [pool.apply(describe, args=(self.features[pd.notna(self.features[feature])][var],), 
#                                  kwds={'nan_policy':'omit','name':var})
#                        for var in self.features.columns.drop(feature)
#                        if pd.api.types.is_numeric_dtype(self.features[var].dtype)]
#            dic_output[feature] = pd.concat(results_missing + results, axis=1)
#            
#        pool.close()
#        self.__lst_operations.append('missing_data_statistics')
#        return dic_output
        pass

    
        
    def visualize(self, bln_show = False, bln_export = True, str_file_path = 'output.png', **kwargs):
        numeric_data = self.features[self.features_by_data_type_enums[ENUM_DATA_TYPE.NUMERIC]]
        for col in numeric_data.columns:
            sns_plot = sns.pairplot(col, **kwargs)
        if bln_show:
            plt.show()
        if bln_export:
            sns_plot.savefig(str_file_path)
        
    def write_report(self, str_operation = 'initial', str_format = 'html'):
        # Initial Data Analysis (IDA)
        # 1. number of variables and their data types
        # 2. descriptive statistics of variables, omitting missing data
        # 3. normality tests 
        # 4. missing data descriptive statistics and test results
        #    (completely random, random or not random)
        # 5. description of missing data treatment
        # 6. description of data normalization methodology
        # 7. selected cross validator
        
#        if str_operation == 'initial':
#            str_output = 'Dataset contains {n_features} {features_plural} and \
#                    {n_targets} {targets_plural}.'.format(n_features=len(self.features_info),
#                    n_targets=len(self.targets_info), 
#                    features_plural=gen_plural('feature', len(self.features_info)),
#                    targets_plural=gen_plural('target', len(self.targets_info)))      

        pass
 


def split_data_set(df_data, y_col_names):
    if isinstance(y_col_names, str) and (not isinstance(y_col_names,list)):
        lst_y_col_names = [y_col_names]
    else:
        lst_y_col_names = y_col_names
    
    return df_data.drop(columns=lst_y_col_names), df_data[lst_y_col_names]
    
class DataCrossValidator(object):
    @conditional_decorator(dec_calculate_time, IS_DEVELOPMENT)
    def __init__(self, enum_cross_validation_method = ENUM_CROSS_VALIDATION_METHOD.STRATIFIED_K_FOLD,
                 enum_data_set_type = ENUM_DATA_SET_TYPE.CROSS_SECTIONAL,
                 **kwargs):
        
        self.cross_validator = None
                    
        self.enum_cross_validation_method = enum_cross_validation_method
        self.enum_data_set_type = enum_data_set_type
        
        if self.enum_cross_validation_method is ENUM_CROSS_VALIDATION_METHOD.K_FOLD:
            self.cross_validator = KFold(**kwargs)
        elif self.enum_cross_validation_method is ENUM_CROSS_VALIDATION_METHOD.REPEATED_K_FOLD:
            self.cross_validator = RepeatedKFold(**kwargs)
        elif self.enum_cross_validation_method is ENUM_CROSS_VALIDATION_METHOD.LEAVE_ONE_OUT:
            self.cross_validator = LeaveOneOut()
        elif self.enum_cross_validation_method is ENUM_CROSS_VALIDATION_METHOD.LEAVE_P_OUT:
            self.cross_validator = LeavePOut(**kwargs)
        elif self.enum_cross_validation_method is ENUM_CROSS_VALIDATION_METHOD.SHUFFLE_SPLIT:
            self.cross_validator = ShuffleSplit(**kwargs)
        elif self.enum_cross_validation_method is ENUM_CROSS_VALIDATION_METHOD.STRATIFIED_K_FOLD:
            self.cross_validator = StratifiedKFold(**kwargs)
        elif self.enum_cross_validation_method is ENUM_CROSS_VALIDATION_METHOD.STRATIFIED_SHUFFLE_SPLIT:
            self.cross_validator = StratifiedShuffleSplit(**kwargs)
        else:
            logger.error('`enum_cross_validation_method` not supported!')
        
    def split(self, X, y=None):
        return self.cross_validator.split(X, y)
    
    def get_n_splits(self):
        return self.cross_validator.get_n_splits()

   

def get_data_type_enum(df_data):
    if pd.api.types.is_numeric_dtype(df_data):
        return ENUM_DATA_TYPE.NUMERIC
    elif pd.api.types.is_categorical_dtype(df_data):
        return ENUM_DATA_TYPE.CATEGORICAL
    elif pd.api.types.is_string_dtype(df_data):
        return ENUM_DATA_TYPE.TEXTUAL
    elif pd.api.types.is_datetime64_any_dtype(df_data):
        return ENUM_DATA_TYPE.DATE
    else:
        return None
 