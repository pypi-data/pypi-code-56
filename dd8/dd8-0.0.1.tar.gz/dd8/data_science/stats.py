# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 13:27:42 2019

@author: yuanq
"""

# standard packages
import numpy as np
import pandas as pd
#import warnings
import multiprocessing as mp
import math
#import tsfresh 
import scipy
import astropy
import enum
from scipy.stats import shapiro, normaltest, anderson
    
# custom packages
from .. import modUtils3 as utils
from .. import modPandasUtils3 as pdu
from .. import modGlobal3 as glob
from .modDSEnums3 import *

logger = utils.get_basic_logger(__name__, glob.LOG_PRINT_LEVEL)



class DescriptiveStatistics(object):
    def __init__(self, df_data,
                 enum_data_set_type,
                 enum_data_type):
        logger.debug('instantiating `DescriptiveStatistics` object...')
        self.data = df_data
        self.enum_data_set_type = enum_data_set_type
        self.enum_data_type = enum_data_type
        if isinstance(self.data, pd.DataFrame):
            self.summary = pd.DataFrame(self.describe(), columns=self.data.columns)
        elif isinstance(self.data, pd.Series):
            self.summary = pd.DataFrame(self.describe(), columns=[self.data.name])
        else:
            self.summary = pd.DataFrame(self.describe())
        
    
    def describe(self, **kwargs):
        if self.enum_data_set_type is ENUM_DATA_SET_TYPE.CROSS_SECTIONAL:
            logger.debug('cross-sectional data set detected')
            if self.enum_data_type is ENUM_DATA_TYPE.NUMERIC:
                logger.debug('numeric data type detected')                
                return describe_numeric(self.data.values)
            elif self.enum_data_type is ENUM_DATA_TYPE.CATEGORICAL:
                logger.debug('categorical data type detected')
                return describe_categorical(self.data)
            elif self.enum_data_type is ENUM_DATA_TYPE.TEXTUAL:
                logger.debug('textual data type detected')
                pass
            elif self.enum_data_type is ENUM_DATA_TYPE.DATE:
                logger.debug('date data type detected')
                return describe_date(self.data)
            
        elif self.enum_data_set_type is ENUM_DATA_SET_TYPE.TIME_SERIES:
            logger.debug('time series data set detected')
            pass
        elif self.enum_data_set_type is ENUM_DATA_SET_TYPE.TEXT:
            logger.debug('text data set detected')
            pass
        elif self.enum_data_set_type is ENUM_DATA_SET_TYPE.IMAGE:
            logger.debug('image data set detected')
            pass
        
def describe_numeric(npa_data, 
                     axis=0, 
                     ddof=1, 
                     bias=True, 
                     nan_policy='propagate', 
                     lst_percentiles=[25., 50., 75.],
                     name=None):
    lst_output = []
    scipy_desc = scipy.stats.describe(npa_data, axis=axis, ddof=ddof, bias=bias,
                                      nan_policy=nan_policy)
    if nan_policy == 'omit':        
        percentiles = np.nanpercentile(npa_data, q=lst_percentiles, axis=axis)
        npa_data = npa_data[~np.isnan(npa_data)]
    else:        
        percentiles = np.percentile(npa_data, q=lst_percentiles, axis=axis)
    
    lst_output.append(['count', scipy_desc.nobs])
    lst_output.append(['mean', scipy_desc.mean])
    lst_output.append(['median', np.median(npa_data, axis=axis)])
    lst_output.append(['std', np.sqrt(scipy_desc.variance)])
    lst_output.append(['variance', scipy_desc.variance])
    lst_output.append(['min', scipy_desc.minmax[0]])
    for i in range(len(lst_percentiles)):
        lst_output.append([str(lst_percentiles[i])+'%', percentiles[i]])
    lst_output.append(['max', scipy_desc.minmax[1]])
    lst_output.append(['skewness', scipy_desc.skewness]) 
    skewness_se = get_skewness_se(scipy_desc.nobs)    
    lst_output.append(['skewness_standard_error', skewness_se]) 
    lst_output.append(['skewness_to_standard_error', abs(scipy_desc.skewness/skewness_se)]) 
    lst_output.append(['kurtosis', scipy_desc.kurtosis])
    kurtosis_se = get_kurtosis_se(scipy_desc.nobs)
    lst_output.append(['kurtosis_standard_error', kurtosis_se])
    lst_output.append(['kurtosis_to_standard_error', abs(scipy_desc.kurtosis/kurtosis_se)])
    lst_output.append(['shapiro-wilk_p_value', scipy.stats.shapiro(npa_data)[1]])
    lst_output.append(['D_Agostino_p_value', scipy.stats.normaltest(npa_data,axis=axis, nan_policy=nan_policy)[1]])
    lst_output = list(zip(*lst_output))
    output = pd.Series(lst_output[1], index=lst_output[0])
    if name:
        output.rename(name, inplace=True)
        
    return output

def describe_categorical(df_data):    
    return df_data.describe()

def describe_date(df_data, name=None):
    lst_output = []
    series_data = df_data
    lst_output.append(['count', series_data.shape[0]])
    lst_output.append(['null', series_data.isna().sum()])
    lst_output.append(['unique_values', series_data.unique().shape[0]])
    lst_output.append(['unique_days', series_data.dt.normalize().unique().shape[0]])
    lst_output.append(['min', series_data.min()])
    lst_output.append(['max', series_data.max()])
    index = series_data.dt.strftime('%a').value_counts().index.to_list()
    values = series_data.dt.strftime('%a').value_counts().to_list()
    for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        for i in range(len(index)):
            if index[i] == day:
                lst_output.append([index[i],values[i]])
                break
    index = series_data.dt.strftime('%b').value_counts().index.to_list()
    values = series_data.dt.strftime('%b').value_counts().to_list()
    for day in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec']:
        for i in range(len(index)):
            if index[i] == day:
                lst_output.append([index[i],values[i]])
                break    
            
    index = series_data.dt.strftime('%H').value_counts().index.to_list()
    values = series_data.dt.strftime('%H').value_counts().to_list()
    for day in ['00', '01', '02', '03', '04', '05', '06', '07', '08',
                '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20', '21', '22', '23']:
        for i in range(len(index)):
            if index[i] == day:
                lst_output.append([index[i],values[i]])
                break 
            
    output = pd.Series(lst_output[1], index=lst_output[0])
    if name:
        output.rename(name, inplace=True)
        
    return output

#class DescriptiveStatistics(object):
#    def __init__(self, df_data):
#        self.data = df_data
#        self.enum_data_type = pdu.get_data_type_enum(df_data)        
#
#    def describe(self, **kwargs):
#        ## check kwargs exists in subsequent function calls
#        
#        if self.enum_data_type is ENUM_DATA_TYPE.NUMERIC:
#            
#            pass
#            
#        elif self.enum_data_type is ENUM_DATA_TYPE.CATEGORICAL:
#            pass
#        elif self.enum_data_type is ENUM_DATA_TYPE.TEXTUAL:
#            pass
#        else:
#            logger.error(str(self.enum_data_type) + ' data type not supported.')
#        
#    def summary(self):
#        pass
#    
#    def percentile(self, lst_percentiles, 
#                   **kwargs):
#        if self.nan_policy == 'omit':        
#            percentiles = np.nanpercentile(self.data, 
#                                           q=lst_percentiles, 
#                                           axis=self.axis,
#                                           **kwargs)            
#        else:        
#            percentiles = np.percentile(self.data, 
#                                        q=lst_percentiles, 
#                                        axis=self.axis,
#                                        **kwargs)
#        return percentiles
#    
#    @staticmethod
#    def scipy_describe(self, npa_data,
#                       axis = 0,
#                       ddof = 1,
#                       bias = True,
#                       nan_policy = 'propagate'):
#        
#        return scipy.stats.describe(npa_data, 
#                                    axis=axis, 
#                                    ddof=ddof,
#                                    bias = bias,
#                                    nan_policy = nan_policy)
#        
#        
#        
#        ## Attributes
#        #  Public
#        #   self.data
#        #   self.shape
#        #   self.enum_data_type
#        #   self.names
#        #   self.summary
#        #  Private
#        #   self.__kwargs
#        
#        if isinstance(df_data, pd.DataFrame):
#            pass
#        elif isinstance(df_data, pd.Series):
#            pass
#        elif isinstance(df_data, np.ndarray):
#            pass
#            
#            
#        self.data = df_data
#        if not axis:
#            self.shape = (1,)
#        elif axis == 0:
#            self.shape = (self.data.shape[1], )
#        elif axis == 1:
#            self.shape = (self.data.shape[0], )        
#        
#        self.enum_data_type = pdu.get_data_type_enum(df_data)
#        self.names = names
#        self.summary = dict()
#        self.__kwargs = kwargs        
#        
#    def describe(self, **kwargs):
#        if self.enum_data_type is ENUM_DATA_TYPE.NUMERIC:
#            self.summary[self.enum_data_type] = self.describe_continuous(self.data, **kwargs)            
#        elif self.enum_data_type is ENUM_DATA_TYPE.CATEGORICAL:
#            pass
#        elif self.enum_data_type is ENUM_DATA_TYPE.TEXTUAL:
#            pass
#        return self.summary
#        
#    def describe_categorical():
#        pass
#    
#    def describe_text():
#        pass
#    
#    def describe_continuous(self,
#                            npa_data, 
#                            axis=0, 
#                            ddof=1, 
#                            bias=True, 
#                            nan_policy='propagate', 
#                            lst_percentiles=[25., 50., 75.],
#                            name=None):
#        lst_output = []
#        scipy_desc = scipy.stats.describe(npa_data, axis=axis, ddof=ddof, bias=bias,
#                                          nan_policy=nan_policy)
#        if nan_policy == 'omit':        
#            percentiles = np.nanpercentile(npa_data, q=lst_percentiles, axis=axis)
#            npa_data = npa_data[~np.isnan(npa_data)]
#        else:        
#            percentiles = np.percentile(npa_data, q=lst_percentiles, axis=axis)
#        
#        lst_output.append(['count', scipy_desc.nobs])
#        lst_output.append(['mean', scipy_desc.mean])
#        lst_output.append(['median', np.median(npa_data, axis=axis)])
#        lst_output.append(['std', np.sqrt(scipy_desc.variance)])
#        lst_output.append(['variance', scipy_desc.variance])
#        lst_output.append(['min', scipy_desc.minmax[0]])
#        for i in range(len(lst_percentiles)):
#            lst_output.append([str(lst_percentiles[i])+'%', percentiles[i]])
#        lst_output.append(['max', scipy_desc.minmax[1]])
#        lst_output.append(['skewness', scipy_desc.skewness]) 
#        skewness_se = get_skewness_se(scipy_desc.nobs)    
#        lst_output.append(['skewness_standard_error', skewness_se]) 
#        lst_output.append(['skewness_to_standard_error', abs(scipy_desc.skewness/skewness_se)]) 
#        lst_output.append(['kurtosis', scipy_desc.kurtosis])
#        kurtosis_se = get_kurtosis_se(scipy_desc.nobs)
#        lst_output.append(['kurtosis_standard_error', kurtosis_se])
#        lst_output.append(['kurtosis_to_standard_error', abs(scipy_desc.kurtosis/kurtosis_se)])
#        lst_output.append(['shapiro-wilk_p_value', scipy.stats.shapiro(npa_data)[1]])
#        lst_output.append(['D_Agostino_p_value', scipy.stats.normaltest(npa_data,axis=axis, nan_policy=nan_policy)[1]])
#        lst_output = list(zip(*lst_output))
#        output = pd.Series(lst_output[1], index=lst_output[0])
#        if name:
#            output.rename(name, inplace=True)
#            
#        return output
        


def get_skewness_se(n_samples):
    return  math.sqrt((6.0 * n_samples * (n_samples-1.0)) / 
                      ((n_samples-2.0) * (n_samples+1.0) * (n_samples+3.0)))
    
def get_kurtosis_se(n_samples):
    return 2 * get_skewness_se(n_samples) * math.sqrt(
            (n_samples * n_samples - 1.0) / ((n_samples-3.0)*(n_samples+5.0)))



def describe(npa_data, 
             axis=0, 
             ddof=1, 
             bias=True, 
             nan_policy='propagate', 
             lst_percentiles=[25., 50., 75.],
             name=None):
    lst_output = []
    scipy_desc = scipy.stats.describe(npa_data, axis=axis, ddof=ddof, bias=bias,
                                      nan_policy=nan_policy)
    if nan_policy == 'omit':        
        percentiles = np.nanpercentile(npa_data, q=lst_percentiles, axis=axis)
        npa_data = npa_data[~np.isnan(npa_data)]
    else:        
        percentiles = np.percentile(npa_data, q=lst_percentiles, axis=axis)
    
    lst_output.append(['count', scipy_desc.nobs])
    lst_output.append(['mean', scipy_desc.mean])
    lst_output.append(['median', np.median(npa_data, axis=axis)])
    lst_output.append(['std', np.sqrt(scipy_desc.variance)])
    lst_output.append(['variance', scipy_desc.variance])
    lst_output.append(['min', scipy_desc.minmax[0]])
    for i in range(len(lst_percentiles)):
        lst_output.append([str(lst_percentiles[i])+'%', percentiles[i]])
    lst_output.append(['max', scipy_desc.minmax[1]])
    lst_output.append(['skewness', scipy_desc.skewness]) 
    skewness_se = get_skewness_se(scipy_desc.nobs)    
    lst_output.append(['skewness_standard_error', skewness_se]) 
    lst_output.append(['skewness_to_standard_error', abs(scipy_desc.skewness/skewness_se)]) 
    lst_output.append(['kurtosis', scipy_desc.kurtosis])
    kurtosis_se = get_kurtosis_se(scipy_desc.nobs)
    lst_output.append(['kurtosis_standard_error', kurtosis_se])
    lst_output.append(['kurtosis_to_standard_error', abs(scipy_desc.kurtosis/kurtosis_se)])
    lst_output.append(['shapiro-wilk_p_value', scipy.stats.shapiro(npa_data)[1]])
    lst_output.append(['D_Agostino_p_value', scipy.stats.normaltest(npa_data,axis=axis, nan_policy=nan_policy)[1]])
    lst_output = list(zip(*lst_output))
    output = pd.Series(lst_output[1], index=lst_output[0])
    if name:
        output.rename(name, inplace=True)
        
    return output



class NormalityTests(object):
    def __init__(self, data, alpha = 0.05):
        self.__data = data
        self.__count = len(data)
        self.__alpha = alpha
        
        
        self.__dic_results = dict()
    
    def __del__(self):
        pass
    
    def __str__(self):
        pass
    
    def __len__(self):
        pass
    
    def get_data(self):
        return self.__data
    
    def get_alpha(self):
        return self.__alpha
    
    def set_alpha(self, alpha):
        self.__alpha = alpha
        return self.__alpha
    
    

    

        
        
        
    
    def is_shapiro_norm(self):
        stat, p = shapiro(self.__data)
        self.__dic_results['shapiro'] = {'test_statistic':stat, 
                                         'p-value':p}
        return p >= self.__dbl_alpha
    
    def is_kstest_norm(self):
        stat, p = normaltest(self.__data)
        self.__dic_results['kstest'] = {'test_statistic':stat, 'p-value':p}
    
        return p >= self.__dbl_alpha
        
    def is_anderson_norm(self):
        result = anderson(self.__data)
        
        for i in range(len(result.critical_values)):
            pass

@utils.conditional_decorator(utils.dec_calculate_time, glob.IS_DEVELOPMENT) 
def get_missing_values_index(df_data):
    if len(df_data.shape)==1:
        return pd.isnull(df_data).nonzero()[0]
    elif len(df_data.shape)==2:
        return pd.isnull(df_data).any(1).nonzero()[0]
    else:
        logger.debug('Dataframes with more than 2 dimensions are not supported.')
 
def gen_preferred_model_settings(self, enum_model, obj_data_prep):
    dic_settings = dict()
    cat_count = len(obj_data_prep.targets.unique())
    if enum_model == ENUM_MODEL.LOGISTIC_REGRESSION:            
        if cat_count!=2:
            dic_settings['solver'] = 'saga'    
        else:
            dic_settings['solver'] = 'liblinear'    
        
        
        if obj_data_prep.features_to_sample_size_ratio >= 1.0:
            dic_settings['dual'] = True
        else:
            dic_settings['dual'] = False
        
        dic_settings['tol'] = 1e-4
        dic_settings['C'] = 1.0
        dic_settings['fit_intercept'] = True
        dic_settings['intercept_scaling'] = 1.0
        dic_settings['class_weight'] = None
        dic_settings['random_state'] = None
        
        dic_settings['max_iter'] = 100
        dic_settings['multi_class'] = 'auto'
        dic_settings['verbose'] = 0
        dic_settings['warm_start'] = False
        dic_settings['n_jobs'] = None
        dic_settings['l1_ratio'] = None
    
    return dic_settings

#def describe(npa_data, 
#             axis=0, 
#             ddof=1, 
#             bias=True, 
#             nan_policy='propagate', 
#             lst_percentiles=[25., 50., 75.],
#             name=None):
#    lst_output = []
#    scipy_desc = scipy.stats.describe(npa_data, axis=axis, ddof=ddof, bias=bias,
#                                      nan_policy=nan_policy)
#    if nan_policy == 'omit':
#        percentiles = np.nanpercentile(npa_data, q=lst_percentiles, axis=axis)
#    else:
#        percentiles = np.percentile(npa_data, q=lst_percentiles, axis=axis)
#    
#    lst_output.append(['count', scipy_desc.nobs])
#    lst_output.append(['mean', scipy_desc.mean])
#    lst_output.append(['median', np.median(npa_data, axis=axis)])
#    lst_output.append(['std', np.sqrt(scipy_desc.variance)])
#    lst_output.append(['variance', scipy_desc.variance])
#    lst_output.append(['min', scipy_desc.minmax[0]])
#    for i in range(len(lst_percentiles)):
#        lst_output.append([str(lst_percentiles[i])+'%', percentiles[i]])
#    lst_output.append(['max', scipy_desc.minmax[1]])
#    lst_output.append(['skewness', scipy_desc.skewness]) 
#    lst_output.append(['kurtosis', scipy_desc.kurtosis])
#    lst_output = list(zip(*lst_output))
#    output = pd.Series(lst_output[1], index=lst_output[0])
#    if name:
#        output.rename(name, inplace=True)
#        
#    return output

def describe_parallel(df_data, 
                         axis=0, 
                         ddof=1, 
                         bias=True, 
                         nan_policy='propagate', 
                         lst_percentiles=[25., 50., 75.],
                         name=None,
                         pool=None):
    pass

def get_scipy_distributions():
    from scipy.stats._continuous_distns import _distn_names
    return [getattr(scipy.stats, distname) for distname in _distn_names]

def fit_distribution(scipy_distribution, data, bins=200):
    try:
        logger.info('`fit_distribution` - Start')
        logger.info('Fitting ' + scipy_distribution.name + '...' )
        y, x = np.histogram(data, bins=bins, density=True)
        x = (x + np.roll(x, -1))[:-1] / 2.0
        params = scipy_distribution.fit(data)
        if len(params)>2:
            arg = params[:-2]
        else:
            arg = []
        loc = params[-2]
        scale = params[-1]
        pdf = scipy_distribution.pdf(x, loc=loc, scale=scale, *arg)
        sse = np.sum(np.power(y - pdf, 2.0))
        logger.info('Fitting of ' + scipy_distribution.name + ''' completed.\n
                    Fitted parameters: ''' + str(params) + '''\n
                    Sum of Squared Errors: ''' +  str(sse))
        logger.info('`fit_distribution` - End')
        return scipy_distribution, params, sse
    except:
        logger.warning('Failed to fit ' + str(scipy_distribution.name))
        return scipy_distribution, None, None

def get_best_fit_distribution(data, bins=None):    
    logger.info('`get_best_fit_distribution_multi` - Start')
    if not bins:
        bins = math.ceil(len(data)**0.5)
    
    lst_distributions = get_scipy_distributions()
    best_distribution = scipy.stats.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    pool = mp.Pool(processes = mp.cpu_count()-1)
    try:    
        logger.info('Attempting to fit distributions via multiprocessing.')
        results = [pool.apply_async(fit_distribution, args=(distribution, data, bins)) 
                        for distribution in lst_distributions]
        outputs = [result.get() for result in results]
        for output in outputs:
            if output[2]:
                if best_sse > output[2] > 0:
                    best_distribution = output[0]
                    best_params = output[1]
                    best_sse = output[2]
    except:
        logger.warning('Failed to fit distributions via multiprocessing.')
        logger.info('Attempting to fit distributions using single core...')
        try:
            y, x = np.histogram(data, bins=bins, density=True)
            x = (x + np.roll(x, -1))[:-1] / 2.0
            best_distribution = scipy.stats.norm
            best_params = (0.0, 1.0)
            best_sse = np.inf
            # Estimate distribution parameters from data
            for distribution in lst_distributions:        
                # Try to fit the distribution
        
#                # Ignore warnings from data that can't be fit
#                with warnings.catch_warnings():
#                    warnings.filterwarnings('ignore')
    
                # fit dist to data
                params = distribution.fit(data)
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse
        except:
            logger.warning('Failed to fit distributions via single core.')
    finally:
        pool.close()
    
    logger.info('`get_best_fit_distribution_multi` - End')
    return best_distribution.name, best_params, best_sse



if __name__ == '__main__':
    import time
    start_time = time.time()
    data = np.random.normal(0.0,1.0,1000)
    results = get_best_fit_distribution(data)
    print(time.time() - start_time)
       
        
#import warnings
#import numpy as np
#import pandas as pd
#import scipy.stats as st
#import statsmodels as sm
#import matplotlib
#import matplotlib.pyplot as plt
#
#matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
#matplotlib.style.use('ggplot')
#
## Create models from data
#def best_fit_distribution(data, bins=200, ax=None):
#    """Model data by finding best fit distribution to data"""
#    # Get histogram of original data
#    y, x = np.histogram(data, bins=bins, density=True)
#    x = (x + np.roll(x, -1))[:-1] / 2.0
#
#    # Distributions to check
#    DISTRIBUTIONS = [        
#        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
#        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
#        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
#        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
#        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
#        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
#        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
#        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
#        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
#        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
#    ]
#
#    # Best holders
#    best_distribution = st.norm
#    best_params = (0.0, 1.0)
#    best_sse = np.inf
#
#    # Estimate distribution parameters from data
#    for distribution in DISTRIBUTIONS:
#
#        # Try to fit the distribution
#        try:
#            # Ignore warnings from data that can't be fit
#            with warnings.catch_warnings():
#                warnings.filterwarnings('ignore')
#
#                # fit dist to data
#                params = distribution.fit(data)
#
#                # Separate parts of parameters
#                if len(params)>2:
#                   arg = params[:-2]
#                else:
#                    arg = []
#                loc = params[-2]
#                scale = params[-1]
#
#                # Calculate fitted PDF and error with fit in distribution
#                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
#                sse = np.sum(np.power(y - pdf, 2.0))
#
#                # if axis pass in add to plot
#                try:
#                    if ax:
#                        pd.Series(pdf, x).plot(ax=ax)
#                    end
#                except Exception:
#                    pass
#
#                # identify if this distribution is better
#                if best_sse > sse > 0:
#                    best_distribution = distribution
#                    best_params = params
#                    best_sse = sse
#
#        except Exception:
#            pass
#
#    return (best_distribution.name, best_params)
#
#def make_pdf(dist, params, size=10000):
#    """Generate distributions's Probability Distribution Function """
#
#    # Separate parts of parameters
#    arg = params[:-2]
#    loc = params[-2]
#    scale = params[-1]
#
#    # Get sane start and end points of distribution
#    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
#    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)
#
#    # Build PDF and turn into pandas Series
#    x = np.linspace(start, end, size)
#    y = dist.pdf(x, loc=loc, scale=scale, *arg)
#    pdf = pd.Series(y, x)
#
#    return pdf
#
## Load data from statsmodels datasets
#data = pd.Series(sm.datasets.elnino.load_pandas().data.set_index('YEAR').values.ravel())
#
## Plot for comparison
#plt.figure(figsize=(12,8))
#ax = data.plot(kind='hist', bins=50, normed=True, alpha=0.5, color=plt.rcParams['axes.color_cycle'][1])
## Save plot limits
#dataYLim = ax.get_ylim()
#
## Find best fit distribution
#best_fit_name, best_fit_params = best_fit_distribution(data, 200, ax)
#best_dist = getattr(st, best_fit_name)
#
## Update plots
#ax.set_ylim(dataYLim)
#ax.set_title(u'El Niño sea temp.\n All Fitted Distributions')
#ax.set_xlabel(u'Temp (°C)')
#ax.set_ylabel('Frequency')
#
## Make PDF with best params 
#pdf = make_pdf(best_dist, best_fit_params)
#
## Display
#plt.figure(figsize=(12,8))
#ax = pdf.plot(lw=2, label='PDF', legend=True)
#data.plot(kind='hist', bins=50, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)
#
#param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
#param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
#dist_str = '{}({})'.format(best_fit_name, param_str)
#
#ax.set_title(u'El Niño sea temp. with best fit distribution \n' + dist_str)
#ax.set_xlabel(u'Temp. (°C)')
#ax.set_ylabel('Frequency')
    