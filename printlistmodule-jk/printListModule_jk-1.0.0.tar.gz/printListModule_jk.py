#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# recursive print function
def rec_print_list(lst):
    for i in lst:
        if(isinstance(i, list)):
            rec_print_list(i)
        else:
            print(i)


