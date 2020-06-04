# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 13:17:13 2020

@author: yuanq
"""

import numpy as np
from abc import ABC, abstractmethod
import math

from dd8 import LOG_PRINT_LEVEL, LOG_WRITE_LEVEL, IS_PRODUCTION
from dd8.utility.utils import get_basic_logger, dec_conditional_decorator, dec_calculate_time

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

class Tree(ABC):
    """
    Abstract Base Class for tree-based classes. Ensure implementation of the
    `diffuse` and `traverse` methods.    
    """
    def __init__(self, int_steps, dbl_initial):
        self.steps = int_steps
        self.initial = dbl_initial
        self.tree = None
    
    @abstractmethod
    def diffuse(self):
        pass
    
    @abstractmethod
    def traverse(self):
        pass

class BinomialTree(Tree):
    """
    Creates a binomial lattice structure.
    """    
    def __init__(self, int_steps, dbl_initial, dbl_u, dbl_d):
        super().__init__(int_steps, dbl_initial)
        self.nodes = 2*self.steps + 1
        self.u = dbl_u
        self.d = dbl_d        
        self.tree = np.zeros(self.nodes)
      
    @dec_conditional_decorator(dec_calculate_time, (not IS_PRODUCTION))
    def diffuse(self):
        self.tree[0] = self.initial * self.u ** self.steps
        for i in range(self.nodes)[1:]:
            self.tree[i] = self.tree[i-1]*self.d
        return self.tree
    
    def traverse(self):
#        odds = self.tree
#        while len(odds)>1:
#            yield odds[::2]
#            odds = odds[1:-1]
        yield self.tree[::2]
        i=1
        while i<=self.steps:
            yield self.tree[i:-1][::2]
            i+=1            
    
class BinomialCRRTree(BinomialTree):
    def __init__(self, int_steps, dbl_initial, dbl_sigma, dbl_dt):
        self.sigma = dbl_sigma
        self.dt = dbl_dt
        super().__init__(int_steps, dbl_initial, 
             math.exp(self.sigma*(self.dt**0.5)),
             math.exp(-self.sigma*(self.dt**0.5)))
    
    
    
    
#class Tree(PricingModel):
#    def __init__(self,
#                 enum_option_type,
#                 enum_call_put,
#                 int_steps,
#                 dbl_initial_price,
#                 dbl_strike_price,
#                 dbl_time_to_maturity,
#                 dbl_riskfree_rate,
#                 dbl_volatility, 
#                 dbl_dividend_yield):
#        self.__enum_option_type = enum_option_type
#        self.__enum_call_put = enum_call_put
#        self.__int_steps = int(int_steps)
#        self.__dbl_initial_price = float(dbl_initial_price)
#        self.__dbl_strike_price = float(dbl_strike_price)
#        self.__dbl_time_to_maturity = float(dbl_time_to_maturity)
#        self.__dbl_riskfree_rate = float(dbl_riskfree_rate)
#        self.__dbl_volatility = float(dbl_volatility)
#        self.__dbl_dividend_yield = float(dbl_dividend_yield)
#        
#        self.__dbl_price = None
#        
#    def __len__(self):
#        pass
#    
#    def __repr__(self):
#        pass
#    
#    def __str__(self):
#        pass
#    
#    def price(self):       
#        time_step = self.__dbl_time_to_maturity / self.__int_steps
#        u = math.exp((self.__dbl_riskfree_rate - 0.5 * (self.__dbl_volatility**2)) 
#                        * time_step + self.__dbl_volatility*(time_step**0.5))
#        d = math.exp((self.__dbl_riskfree_rate - 0.5 * (self.__dbl_volatility**2)) 
#                            * time_step - self.__dbl_volatility*(time_step**0.5))
#        
#        drift = math.exp((self.__dbl_riskfree_rate-self.__dbl_dividend_yield)*time_step)
#        q = (drift - d) / (u-d)
#        
#        if self.__enum_call_put == enums.ENUM_CALL_PUT.CALL:
#            cp = 1.0
#        elif self.__enum_call_put == enums.ENUM_CALL_PUT.PUT:
#            cp = -1.0
#        
#        stkval = np.zeros((self.__int_steps+1, self.__int_steps+1))
#        optval = np.zeros((self.__int_steps+1, self.__int_steps+1))
#        
#        stkval[0,0] = self.__dbl_initial_price
#        for i in range(1, self.__int_steps+1):
#            stkval[i, 0] = stkval[i-1, 0] * u
#            for j in range(1, self.__int_steps+1):
#                stkval[i,j] = stkval[i-1, j-1]*d
#                
#        for j in range(self.__int_steps+1):
#            optval[self.__int_steps,j] = max(0, cp*(stkval[self.__int_steps,j]-self.__dbl_strike_price))
#            
#        for i in range(self.__int_steps-1,-1,-1):
#            for j in range(i+1):
#                optval[i, j] = (q*optval[i+1, j] + (1-q)*optval[i+1, j+1])/drift
#                if self.__enum_option_type == enums.ENUM_OPTION_TYPE.AMERICAN:
#                    optval[i, j] = max(optval[i, j] , cp*(stkval[i, j]-self.__dbl_strike_price))
#                    
#                    
#        self.__dbl_price = optval[0,0]
#        return self.__dbl_price
#    
#    def gen_vega(self, dbl_bump_size = None, enum_bump_method,
#                 enum_finite_difference_method):
#        pass