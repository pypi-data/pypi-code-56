# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 18:37:40 2020

@author: yuanq
"""

import numpy as np

from dd8 import LOG_PRINT_LEVEL, LOG_WRITE_LEVEL
from dd8.utility.utils import get_basic_logger

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

def incremental_search(obj_func, dbl_start, dbl_end, dbl_dx):
    initial_x = dbl_start
    initial_y  = obj_func(initial_x)
    next_x = initial + dbl_dx
    next_y = obj_func(next_x)
    counter = 1
    while np.sign(initial_y) == np.sign(next_y):
        if initial_x >= dbl_end:
            return initial_x - dbl_dx, counter
        
        initial_x = next_x
        initial_y = next_y
        next_x = nex