#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:21:12 2020

@author: yves

    This file is part of Saqqarah.

    Saqqarah is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Saqqarah is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Saqqarah.  If not, see <https://www.gnu.org/licenses/>
"""

import numpy as np
import itertools
from time import time

class Pyramid():
    """ 
    Pyramid with size and number of boxes
    Method get_puzzle give a puzzle with solution
    
    Not clean: rewrtie with getaatr or properties
    """
    
    # stolen in the net (choose)
    # 
    def nCr(self, n, k):
        """
        A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
        """
        if 0 <= k <= n:
            ntok = 1
            ktok = 1
            for t in range(1, min(k, n - k) + 1):
                ntok *= n
                ktok *= t
                n -= 1
            return ntok // ktok
        else:
            return 0

    def __init__(self, size):
        if size < 4:
            raise ValueError("Pyramid Size at least 4")
        # size
        self.n = size
        # n lines of the matrix
        self.n_lines = self.n*(self.n+1)//2
        # calculation matrix from base line to all values
        self.mat = np.empty((self.n_lines,self.n), dtype='int')
        
        # used only to statistical fonctions 
        self.determinants = None

        m_line = 0
        for part in range(self.n,0,-1):
            n_comb = self.n - part
            for line in range(part):
                for case in range(self.n):
                    self.mat[m_line, case] = self.nCr( n_comb, case - line)
                m_line += 1
                
        self.solution = None
        self.puzzle = {}
        
    def get_size(self):
        return self.n
    
    def get_nbr_cases(self):
        return self.n_lines
    
    def get_puzzle(self, difficulty = 2, min=1, max = 9, *, seed = None):
        """
        return a dict { number_of_case : value }
        you can use it to set a puzzle at hand
        """
        if difficulty < 1 or difficulty > 8:
            raise ValueError("difficulty between 1 and 8")
        elif difficulty >  3 and self.n == 4:
            raise ValueError("size too low for difficulty")

        # self.random_cases are cases to fill for the puzzle
        # get nanoseconds of time as reusable seed as fallback
        self.seed = seed or int(str(round(time()*1_000_000))[-9:])
        np.random.seed(seed)
        self.random_cases = np.array(self.__choose_random__(difficulty))
        self.random_cases.transpose()

        # choose values for base line
        self.base_solution = np.random.randint(min, max+1, size=(self.n,1))
        
        # get values for all cases
        self.solution = np.matmul(self.mat, self.base_solution)

        # get index and values for selected cases
        # the visible part of the puzzle
        self.puzzle = { c: int(self.solution[c,0]) for c in self.random_cases }
        
        return self.puzzle

    def __choose_random__(self, difficulty = 2):
        """
        choose at random cases to fill for given difficulty
        """
        lines = list(range(self.n_lines))
        np.random.shuffle(lines)
        iter_mat = itertools.combinations(lines, self.n)
        
        det = 0
        for i,l in enumerate(iter_mat):
            det =  round(abs(np.linalg.det(self.mat[l,])))
            if det == difficulty:
                tries='try' if i==0 else 'tries'
                print(f'Find a puzzle for difficulty {difficulty}, total {i+1} {tries}')
                return tuple(sorted(l))
            if i%100 == 0:
                print(f"Looking for puzzle... {i}", end='\r')
        else:
            raise ValueError("This difficulty was not found with that size")
    
    #####
    # statistical only calculations: all determinants
    # for all choices of cases
    # only det !=0 give a possible puzzle 
    # abs(determinant) is used as a difficulty level 
    #####     
    def __get_determinants__(self):
        """
        list all determinants in self.determinants
        can be long, 9min on my old core i7 for n=8
        """
        lines = list(range(self.n_lines))
        # random.shuffle(lines)
        sel_mat = itertools.combinations(lines, self.n)
        self.determinants =  {}

        for l in sel_mat:
            #l = sorted(l)
            det =  abs(round(np.linalg.det(self.mat[l,])))
            if det in self.determinants:
                self.determinants[det].append(l)
            else:
               self.determinants[det] = [l]
               
    def __nbr_cas__(self):
        return self.nCr(self.n_lines, self.n_lines - self.n)

    def __bilans__(self):
        # can be long
        if not self.determinants:
            self.__get_determinants__()
            
        if 0 in self.determinants:
            n_zeros = len(self.determinants[0])
        else:
            n_zeros = 0
        print(f"{self.__nbr_cas__()} choix possibles dont {n_zeros} impossibles.")
        max_det = max(self.determinants.keys())
        print(f"Déterminant maximal : {max_det}")
