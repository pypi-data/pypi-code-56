# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:59:01 2020

@author: Lim Yuan Qing

SUMMARY
-------


EXTENDED SUMMARY
----------------


ROUTINE LISTINGS
----------------
TimeSeriesData
StationaryTest
ADF

"""

from dd8 import get_basic_logger, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL
from dd8.data_science import Data
from dd8.data_science.enums import ENUM_STATIONARITY_TEST

import pandas as pd
import datetime
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.graphics.tsaplots as tsaplots
from abc import ABC, abstractmethod

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)
   
class TimeSeriesData(Data):
    """
    Each instance contains a time series data set. Provides convenience functions
    to preprocess time series data and consistent interfacing for data modelling
    further down the analytics pipeline. The purpose of the data preprocessing 
    is to achieve stationarity.
    
    Typical workflow:
    1.  Check for missing data / uneven time series
    2.  Perform stationarity tests (ADF, KPSS, PP) to determine if time series 
        is stationary and the cause of non-stationarity
    3.  If stationary
            Done!
        Else
            Go to 4.
    4.  Perform data transformation depending on the cause of non-stationarity
        a.  trend
        b.  seasonality
   
    Attributes
    ----------
    data
    has_datatime_index
    is_monotonic_increasing
    is_monotonic_decreasing
   
    Methods
    -------
       
    """
    def __init__(self, X, y=None):
        self.__data = pd.DataFrame(X)
        self.__has_datetime_index = isinstance(self.__data.index, pd.DatetimeIndex)
        self.__is_monotonic_increasing = self.__data.index.is_monotonic_increasing        
   
    @property
    def data(self):
        return self.__data
   
    @property
    def has_datetime_index(self):
        return self.__has_datetime_index
   
    @property
    def is_monotonic_increasing(self):
        return self.__is_monotonic_increasing
   
    @property
    def is_monotonic_decreasing(self):
        return not self.__is_monotonic_increasing
   
    def is_stationary(self, dbl_p_value=0.05):
        """
        To determine if time series is stationary.
        
        Return
        ------
        dict
            dictionary of dictionaries with the following structure:
            {column_header: {stationarity_test_name: is_stationary}}
        """
        results = dict()
        for col in self.data.columns:
            pass
        
    def seasonal_decompose(self, dic_freq=None, *args, **kwargs):
        """
        Seasonal decomposition using moving averages using 
        `statsmodels.tsa.seasonal.seasonal_decompose`.
        
        Parameters
        ----------
        dic_freq : dict
            dictionary specifying columns to perform seasonal decomposition,
            of the structure {column_name: frequency}
                
        Return
        ------
        dict
            dictionary of `DecomposeResult` objects with the following structure:
            {column_name: decompose_result_object}        
        """
        results = dict()
        if dic_freq:
            for k, v in dic_freq.items():            
                results[k] = seasonal_decompose(self.data[k], freq=v, 
                                                   *args, **kwargs)            
        return results
    
    def plot_acf(self):
        pass
    
    def plot_pacf(self):
        pass

class StationarityTest(ABC):
    """
    Abstract base class for time series stationarity tests. Provides consistent
    interfacing for determining if a time series is stationary under different
    statistical tests.
   
    Attributes
    ----------
    test_statistics
    p_value
    critical_values
    summary
    is_stationary : dict
        returns a dictionary with {column_header : 
            {stationarity_test_name : is_stationary}
            }
   
    Methods
    -------
    """
    def __init__(self):
        pass
           
    @property
    def test_statistics(self):
        pass
    
    @property
    def p_value(self):
        pass
    
    @property
    def critical_values(self):
        pass
    
    @property
    def summary(self):
        pass
    
    @abstractmethod
    def is_stationary(self):
        pass
   
class ADF(StationarityTest):
    """
    Wrapper for `statsmodel.adfuller()` function to provide consistent interfacing
    across different time series stationarity tests.
   
    H0: time series contain a unit root and is non-stationary
    H1: time series does not contain a unit root and is stationary
   
    Disadvantages of ADF test
    1.  The ADF test does not truly tell apart between pure and non-unit root
        generating processes. In long-term moving average processes, the ADF
        test becomes biased in rejecting the null hypothesis.
    2.  There is no fixed methodology in determining the lag length, p. If p is too
        small, the remaining serial correlation in the errors may affect the size
        of the test. If p is too large, the power of the test will deteriorate.
    3.  As deterministic terms are added to the test regressions, the power of 
        unit root test diminishes.
    
    Attributes
    ----------
    maxlag
    regression
    autolag
    store
    regresults
    test_statistics
    used_lag
    number_of_observations
    critical_values
    best_information_criterion
   
    Methods
    -------
    is_stationary(p_value)
        Indicates if time series is stationary at specified (<=) p_value
    """
    def __init__(self, maxlag=None,
                 regression='c',
                 autolag=None,
                 store=True,
                 regresults=True):        
        self.__maxlag = maxlag
        self.__maxlag = maxlag
        self.__regression = regression
        self.__autolag = autolag
        self.__store = store
        self.__regresults = regresults
        self.__test_result = None        
        
    def __str__(self):
        if not self.regresults and not self.store:
            output = 'Augmented Dickey-Fuller Test Results\n\n'
            output += 'ADF test statistic: {test_statistics}\n'
            output += 'p-value: {p_value}\n'
            for k, v in self.raw_results[2].items():
                output += 'Critical value ({crit_val}): {val}\n'.format(crit_val=k, val=v)
                
            return output.format(test_statistics=self.test_statistics,
                                 p_value=self.p_value)
        else:
            return str(self.summary)
    
    @property
    def raw_results(self):
        return self.__test_result
        
    @property
    def maxlag(self):
        return self.__maxlag
   
    @property
    def regression(self):
        return self.__regression
   
    @property
    def autolag(self):
        return self.__autolag
   
    @property
    def store(self):
        return self.__store
   
    @property
    def regresults(self):
        return self.__regresults
   
    @property
    def test_statistics(self):        
        return self.raw_results[0]
   
    @property
    def p_value(self):
        return self.raw_results[1]
   
    @property
    def used_lag(self):
        if not self.regresults and not self.store:
            return self.raw_results[2]
        else:
            return self.raw_results[3].usedlag
   
    @property
    def number_of_observations(self):
        if not self.regresults and not self.store:
            return self.raw_results[3]
        else:
            return self.raw_results[3].nobs
   
    @property
    def critical_values(self):
        if not self.regresults and not self.store:
            return self.raw_results[4]
        else:
            return self.raw_results[3]
   
    @property
    def best_information_criterion(self):
        if not self.regresults and not self.store:
            return self.raw_results[5]
        else:
            return self.raw_results[3].icbest
   
    @property
    def h0(self):
        if not self.regresults and not self.store:
            return None
        else:
            return self.raw_results[3].H0
     
    @property
    def hA(self):
        if not self.regresults and not self.store:
            return None
        else:
            return self.raw_results[3].HA
       
    @property
    def resols(self):
        if not self.regresults and not self.store:
            return None
        else:
            return self.raw_results[3].resols
        
    @property
    def summary(self):
        if not self.regresults and not self.store:
            return None
        else:
            return self.resols.summary()

    def fit(self, X, y=None):        
        self.__test_result = adfuller(X,
                                      self.maxlag,
                                      self.regression,
                                      self.autolag,
                                      self.store,
                                      self.regresults)
   
    def is_stationary(self, p_value):
        return self.__test_result[1]<=p_value

#from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
#from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
#import statsmodels.tsa.seasonal
#import astropy
#import pmdarima
#import enum
#
## custom packages
#from .. import modUtils3 as utils
#
#logger = utils.get_basic_logger(__name__,utils.logging.DEBUG,utils.logging.INFO)
#
#@enum.unique
#class ENUM_LSSA_METHOD(enum.Enum):
#    LOMB_SCARGLE = 1
#    VANICEK = 2
#
#class TimeSeries(object):
#    def __init__(self, df_y, df_X=None, bln_is_ascending=True):
#        self.__df_y = df_y
#        self.__df_X = df_X
#        self.__bln_is_ascending = bln_is_ascending    
#    
#    def __repr__(self):
#        pass
#    
#    def __len__(self):
#        return self.__df_y.shape[0]
#    
#    def is_stationary(self):
#        pass
#    
#    def seasonal_decompose(self,
#                           str_model='additive', 
#                           arr_filt=None, 
#                           int_freq=None, 
#                           bln_two_sided=True, 
#                           int_extrapolate_trend=0):
#        return statsmodels.tsa.seasonal.seasonal_decompose(self.__df_y,
#                                                           model=str_model, 
#                                                           filt=arr_filt, 
#                                                           freq=int_freq, 
#                                                           two_sided=bln_two_sided, 
#                                                           extrapolate_trend=int_extrapolate_trend)
#    
#    
#    def auto_arima(self, lst_start_params=None):
#        return pmdarima.auto_arima(self.__df_y, seasonal=True, m=365, transparams=False, start_params=lst_start_params).summary()
#    
#    def gen_evenly_spaced_series(self, 
#                                 enum_method = ENUM_LSSA_METHOD.LOMB_SCARGLE,
#                                 **kwargs):
#        if enum_method == ENUM_LSSA_METHOD.LOMB_SCARGLE:
#            if '3.1' in astropy.__version__:
#                pass
#            elif '3.2' in astropy.__version__:
#                if kwargs is not None:
#                    model = astropy.timeseries.LombScargle(self.__npa_x, 
#                                                           self.__npa_y, 
#                                                           **kwargs)
#                else:
#                    model = astropy.timeseries.LombScargle(self.__npa_x,
#                                                           self.__npa_y)
#

class PredictiveModel(ABC):
    def __init__(self):
        pass
    
    @property
    def model(self):
        pass
    
    @property
    def summary(self):
        pass
    
    @abstractmethod
    def predict(self):
        pass
    
    @abstractmethod
    def fit(self):
        pass
    

class SarimaxModel(PredictiveModel):
    """
    Wrapper for `statsmodels.tsa.statespace.sarimax.SARIMAX` to provide consistent
    interfacing for data modelling and integration of workflow. The purpose of 
    this wrapper is to facilitate cross-validation and grid search in the model
    selection process.
    """
    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
        self.__model = None
    
    @property
    def model(self):
        return self.__model
    
    def fit(self, y, X=None, **kwargs):
        self.__model = SARIMAX(y, X, *self.__args, **self.__kwargs).fit(**kwargs)
    
    def predict(self, X=None, **kwargs):
        """
        
        """
        pass
    
    
def approximate_freq(time_index):
    diff = time_index.to_series().diff().mean()
    if diff.days > 0:
        return datetime.timedelta(days=diff.days)
    elif diff.seconds > 0:
        return datetime.timedelta(seconds=diff.seconds)
    elif diff.microseconds > 0:
        return datetime.timedelta(microseconds=diff.microseconds)
    else:
        return None

