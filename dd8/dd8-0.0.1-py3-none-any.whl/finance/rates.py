# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:23:54 2020

@author: yuanq
"""

import calendar
import pandas as pd

from dd8 import get_basic_logger, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL
from dd8.finance.quant import Schedule, Interpolater1D
from dd8.finance.enums import ENUM_INTERPOLATION_METHOD, ENUM_DAY_COUNT_CONVENTION

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

DIC_DAY_COUNT_CONVENTION = {
                            'CHF':ENUM_DAY_COUNT_CONVENTION.ACT_360,
                            'EUR':ENUM_DAY_COUNT_CONVENTION.ACT_360,
                            'GBP':ENUM_DAY_COUNT_CONVENTION.ACT_365,
                            'JPY':ENUM_DAY_COUNT_CONVENTION.ACT_360,
                            'USD':ENUM_DAY_COUNT_CONVENTION.ACT_360,
                            'AUD':ENUM_DAY_COUNT_CONVENTION.ACT_360,
                            'CAD':ENUM_DAY_COUNT_CONVENTION.ACT_360,
                            'HKD':ENUM_DAY_COUNT_CONVENTION.ACT_365,
                            'NZD':ENUM_DAY_COUNT_CONVENTION.ACT_360,
                            'SGD':ENUM_DAY_COUNT_CONVENTION.ACT_365,
                            'THB':ENUM_DAY_COUNT_CONVENTION.ACT_365
                            }

class RatesCurve(Schedule):
    def __init__(self, str_currency,
                 npa_start_dates, 
                 npa_end_dates,
                 npa_rates,  
                 enum_compounding_frequency, str_id):
        super().__init__(npa_dates, npa_rates, str_id)
        self.day_count = int_day_count
        self.compounding_frequency = enum_compounding_frequency
        
    def from_date(self, dte_to_interpolate):
        pass
    
    def from_days(self, int_num_of_days):
        pass

class ZeroCurve(RatesCurve):
    def __init__(self, npa_dates, npa_rates,
                 int_day_count,
                 enum_compounding_frequency,
                 str_id=''):
        super().__init__(npa_dates, npa_rates, int_day_count, 
             enum_compounding_frequency, str_id)
        
    def __call__(self, int_days):
        pass

class ForwardCurve(Schedule):
    def __init__(self, npa_dates, npa_rates):
        super().__init__(npa_dates, npa_rates)

class DiscountCurve(RatesCurve):
    """
    Each instance represents a discount curve. Inherits from `quant.Schedule`.
    The discount curve is not unique to any particular product or pricing model,
    and the same instance can be passed as an input parameter to any other
    object that needs to perform discounting. As such, it makes senses to 
    calibrate scipy interpolater on instantiation.
    
    Attributes
    ----------
    currency
    start_dates
    end_dates
    rates
    uid
    days
    day_count_convention
    
    Methods
    -------
    
    """
    def __init__(self, str_currency, 
                 npa_start_dates, 
                 npa_end_dates, 
                 npa_rates, 
                 str_uid=''):
        super().__init__(npa_end_dates, npa_rates, str_uid)
        self.__start_dates = npa_start_dates
        self.__currency = str_currency
        
    @property
    def currency(self):
        return self.__currency
    
    @property
    def start_dates(self):
        return self.__start_dates
    
    @property
    def end_dates(self):
        return self.dates
    
    @property
    def rates(self):
        return self.values
    
    @property
    def uid(self):
        return self.uid
    
    @property
    def days(self):
        return (self.end_dates - self.start_dates).astype('timedelta64[D]')
    
    @property
    def day_count_convention(self):
        return DIC_DAY_COUNT_CONVENTION[self.currency]
    
    def get_rate_from_day(self):
        pass
    
    def get_rate_from_date(self):
        pass
    
    def get_discount_factor_from_day(self):
        pass
    
    def get_discount_factor_from_date(self):
        pass
    
    def __call__(self, date, enum_interpolation_method=None):
        
        
        if not enum_interpolation_method:
            enum_interpolation_method = ENUM_INTERPOLATION_METHOD.LINEAR
        
        __ = self.day_count_convention.split('/')
        if __[0] == 'ACT':
            pass
        else:
            pass
#        
#        
#        if enum_interpolation_method == ENUM_INTERPOLATION_METHOD.LINEAR:
#            
#            return Interpolater1D(ENUM_INTERPOLATION_METHOD.LINEAR)(
#                    calendar.timegm(date), pd.Timestamp(self.dates).values, self.values)