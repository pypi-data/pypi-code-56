# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:36:06 2020

@author: athirasasidharan
"""
#Recursively call print function
def rec_print_list(lst):
    for i in lst:
        if(isinstance(i, list)):
            rec_print_list(i)
        else:
            print(i)
            

