# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:22:59 2020

@author: yuanq
"""

from dd8 import get_basic_logger, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL
from dd8.finance.quant import Schedule, Underlying

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

class Dividend(Schedule):
    """
    Each instance represents one dividend schdule.
    
    Attributes
    ----------
    npa_ex_dates : np.ndarray
        ex-dividend dates in chronological order
    npa_amount : np.ndarray
        dividend amount of the corresponding ex-dividend dates
    """
    def __init__(self, npa_ex_dates, npa_amount):
        super().__init__(npa_ex_dates, npa_amount)
        
    def is_ex_date(self, dte_to_check):
        return dte_to_check in self.dates
    
    def get_div_yield(self, dte_as_at = None):
        pass
    
    def get_div_pv(self, dte_as_at = None):
        pass
    
class Security(Underlying):
    """
    Each instance represents one equity secruity.
    """
    def __init__(self, str_bloombreg_symbol,
                 bln_has_bloomberg=False):
        super().__init__(str_bloombreg_symbol)
        
        