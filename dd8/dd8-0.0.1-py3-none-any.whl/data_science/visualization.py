# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 15:08:33 2019

@author: yuanq
"""

import matplotlib.pyplot as plt

import modDSEnums3 as enm

class Visualize(object):
    def __init__(self, 
                 data, 
                 figure=None,
                 **kwargs):
        self.data = data        
        if figure:
            self.figure = figure
        else:
            self.figure = plt.figure(plt.get_fignums()[-1]+1, **kwargs)
        
    def __del__(self):
        plt.close(self.figure)  
        
    def add_axes(self, str_id, rect, **kwargs):
        self.figure.add_axes(rect, **kwargs)
    
    def get_figure(self):
        return self.figure
    
    def get_figure_num(self):
        return self.figure.number
    
    def save(self, file_type='jpg'):
        pass    
    
    def show(self):
        self.figure.tight_layout()
        self.figure.show()
        
        
if __name__ == '__main__':
    a = plt.figure(1)
    b = plt.figure(2)
    
    
    
    plt.close(a)
    print(plt.get_fignums())
    
    