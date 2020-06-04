# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 22:42:06 2019

@author: LIM YUAN QING
@email: yuanqing87@gmail.com

Classes
-------
VolatilitySurface
Dividend


"""

## Python Modules
from abc import ABC, abstractmethod
import math
import scipy.stats
import scipy.interpolate
import numpy as np
import pandas as pd
import calendar
import datetime

## Custom Modules
import dd8
import dd8.utility.utils as utils
import dd8.finance.enums as enums

## Log Settings
logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)



class Underlying(object):
    def __init__(self, str_bloomberg_symbol):
        self.bloomberg_symbol = str_bloomberg_symbol.upper()
#        info = bbg.bloomberg_bdp(self.__str_bloomberg_symbol,
#                                 ['BPIPE_REFERENCE_SECURITY_CLASS',
#                                  'CRNCY',
#                                  'DVD_CRNCY'])
#        
#        self.__str_asset_class = info[0][0]
#        self.__str_currency = info[0][1]
#        self.__str_dvd_currency = info[0][2]

class Schedule(object):
    """
    Each instance represents a schedule, where a numerical value, such as interest
    rate or cashflow, is associated with a particular date. 
    
    Attributes
    ----------
    dates
    values
    uid 
    """
    def __init__(self, npa_dates, npa_values, str_uid):   
        self.__dates = npa_dates
        self.__values = npa_values
        self.__uid = str_uid
        
    @property
    def dates(self):
        return self.__dates
        
    @property
    def values(self):
        return self.__values
    
    @property
    def uid(self):
        return self.__uid

class Interpolater1D(object):
    def __init__(self, enum_interpolation_method=None):        
        self.interpolation_method = enum_interpolation_method
        
    def __call__(self, value_to_interpolate, x, y, **kwargs):
        if self.interpolation_method == enums.ENUM_INTERPOLATION_METHOD.LINEAR:
            return scipy.interpolate.interp1d(x, y, **kwargs)(value_to_interpolate)
        elif self.interpolation_method == enums.ENUM_INTERPOLATION_METHOD.CUBIC_SPLINE:
            return scipy.interpolate.CubicSpline(x, y, **kwargs)(value_to_interpolate)

class Forward(object):
    """
    Compute the forward rate
    
    Parameters
    ----------
    initial : double
        initial spot value
    risk_free : double
        risk-free rate
    time_to_maturity : double
        time to maturity
    asset_class : ENUM_FORWARD_ASSET_CLASS
        enum to indicate asset class: EQ, FX, IR
        
    Returns
    -------
    float
        forward rate
        
    Raises
    ------
    ValueError
        when an invalid method enum is passed to function
        
    Source(s)
    ---------
    [1] Bloomberg
    """
    def __init__(self, initial, rates_curve, cost_of_carry):
        pass

class PresentValue(object):
    def __init__(self, dte_reference, obj_schedule, obj_discount_curve):
        self.reference_date = dte_reference
        self.schedule = obj_schedule
        self.discount_curve = obj_discount_curve
        
    def pv(self):
        pass
    
    def npv(self):
        pass
    
    

    
    
    



class Portfolio(object):
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
    def __str__(self):
        pass
    
    def __len__(self):
        pass
    
class Trade(object):
    def __init__(self, enum_product_type, dic_trade_param):
        pass
    
    def __repr__(self):
        pass
    
    def __str__(self):
        pass
    
    def __len__(self):
        pass





class Bump(object):
    def __init__(self, dbl_size, 
                 enum_bump_method,
                 enum_finite_difference_method):
        self.size = dbl_size
        self.bump_method = enum_bump_method
        self.finite_difference_method = enum_finite_difference_method

    def bump(self, dbl_original):
        pass        


        



    
    

def discounted_dividend(start_date, end_date, div_dates, div_amount):
    pass

def div_yield(lst_schedule):
    pass

class RiskFreeCurve:
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    def __str__(self):
        pass
    
    def __len__(self):
        pass
    
class MarketConventions:
    def __init__(self, str_market):
        self.__str_market = str_market
        try:
            self.__str_currency = self.gen_currency()
        except KeyError:
            print('Unsupported market.')
            return
    
    def __del__(self):
        print('Object deleted.')
    
    def __str__(self):
        pass
    
    def __len__(self):
        pass
    
    def gen_currency(self):
        return {'UN':'USD',
                    'UQ':'USD',
                    'UW':'USD',
                    'US':'USD',
                    'UP':'USD',
                    'EU':'EUR',
                    'GY':'EUR',
                    'FP':'EUR',
                    'LN':'GBP',
                    'NA':'EUR',
                    'SW':'CHF',
                    'SG':'SGD',
                    'SP':'SGD',
                    'HK':'HKD',
                    'AU':'AUD',
                    'AT':'AUD',
                    'JP':'JPY',
                    'JT':'JPY',
                    'MA':'MYR',
                    'MK':'MYR',
                    'TH':'THB',
                    'TB':'THB'}[self.__str_market]
        
    def gen_calendar_code(self):
        return {'USD':'US',
                'SGD':'SI',
                'MYR':'MA',
                'AUD':'AU',
                'HKD':'HK',
                'JPY':'JN',
                'EUR':'USD'}
        
        
        
def differentiate(f, x, step=0.01, method=enums.ENUM_DERIVATIVE_METHOD.CENTRAL):
    """
    Compute the derivative of f
    
    Parameters
    ----------
    f : object
        function of one variable
    x : double
        point at which to compute derivative
    step : double
        step size in difference formula
    method : ENUM_DERIVATIVE_METHOD
        enum to determine difference formula: CENTRAL, FORWARD, BACKWARD
        
    Returns
    -------
    float
        Difference formula:
            ENUM_DERIVATIVE_METHOD.CENTRAL:  [f(x+step)-f(x-step)]/(2*step)
            ENUM_DERIVATIVE_METHOD.FORWARD:  [f(x+step)-f(x)]/(step)
            ENUM_DERIVATIVE_METHOD.BACKWARD: [f(x)-f(x-step)]/(step)
            
    Raises
    ------
    ValueError
        when an invalid method enum is passed to function
        
    Source(s)
    ---------
    [1] http://www.math.ubc.ca/~pwalls/math-python/differentiation/    
    """
    
    if method == enums.ENUM_DERIVATIVE_METHOD.CENTRAL:
        return (f(x+step)-f(x-step))/(2*step)
    elif method == enums.ENUM_DERIVATIVE_METHOD.FORWARD:
        return (f(x+step)-f(x))/(step)
    elif method == enums.ENUM_DERIVATIVE_METHOD.BACKWARD:
        return (f(x)-f(x-step))/(step)
    else:
        raise ValueError('''method must be ENUM_DERIVATIVE_METHOD.CENTRAL, 
                                 ENUM_DERIVATIVE_METHOD.FORWARD, 
                                 ENUM_DERIVATIVE_METHOD.BACKWARD''')
    
def partial_derivative():
    pass




## Implementation of Cox-Ross-Rubenstein option's pricing model.
#
#from scipy.stats import norm
#import numpy as np
#
##OP inputs as i understand them
#T = 0.25 # time horizon
#M = 2 # quantity of steps
#sigma = 0.1391*np.sqrt(0.25) # volatility
#r0 = 0.0214
#S0 = 2890.30 # initial underlying stock price
#K = 2850 # strike
#
##size M+1 grid of stock prices simulated at time T
#def stock_prices(S0,T,sigma,M):    
#    res = np.zeros(M+1)    
#    t = T*1.0/M # step
#    u = np.exp(sigma*np.sqrt(t)) # up-factor
#    d = 1.0/u
#    dn = d/u
#    res[0] = S0*np.power(u,M) 
#    for i in range(1,M+1):
#        res[i] = res[i-1] * dn
#    return res
#
## terminal payoff from call option
#def payoff(stock_price, K,kind='call'):
#    epsilon = 1.0 if kind == 'call' else -1.0
#    price = np.maximum(epsilon*(stock_price - K), 0)
#    return price
#
## price for European style option using CRR
#def european_crr(S0,K,T,r,sigma,M,kind='call'):
#    #terminal payoff
#    option_price = payoff(stock_prices(S0,T,sigma,M),K,kind)
#    t = T*1.0/M # time_step
#    df = np.exp(-r*t) #discount factor
#    u = np.exp(sigma * np.sqrt(t))
#    d = 1/u
#    p = (np.exp(r*t)-d)/(u-d) # risk neutral probability for up-move        
#    q=1-p    
#    for time_idx in range(M): #move backward in time
#        for j in range(M-time_idx):
#            option_price[j] = df*(p*option_price[j]+q*option_price[j+1])
#    return option_price[0]
#
##analytical check Black-Scholes formula (no dividend nor repo)
#def european_bs(S0,K,T,r,sigma,kind='call'):
#    df = np.exp(-r*T)
#    F = np.exp(r*T)*S0                   # forward price with no dividend or repo
#    m = np.log(F/K)/(sigma * np.sqrt(T)) #moneyness
#    epsilon = 1.0 if kind == 'call' else -1.0
#    d1 = m + 0.5*sigma*np.sqrt(T)
#    d2 = d1 - sigma * np.sqrt(T)
#    Nd1 = norm.cdf(epsilon*d1)
#    Nd2 = norm.cdf(epsilon*d2)
#    return epsilon*df*(F*Nd1-K*Nd2)




if __name__ == '__main__':
    #underlying = Underlying('700 HK EQUITY')
    bsm = BlackScholesModel(enums.ENUM_CALL_PUT.CALL,
                            382.10,
                            380.,
                            90.0/360.0,
                            0.02060,
                            0.27801,
                           0.01064)
    
    print(bsm.gen_greeks_full())
#    bsm2 = eval(bsm.__repr__())
#    print(bsm2)
    
    
    