#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:35:23 2020

@author: ignitarium
"""

# recursive print function
def rec_print_list(lst):
    for i in lst:
        if(isinstance(i, list)):
            rec_print_list(i)
        else:
            print(i)