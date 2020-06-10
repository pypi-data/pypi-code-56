# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:44:26 2020

@author: Intiser Rajoan
"""
L = [1, 2, 3, 5, 45, 90, 120, 143, 145, 170, 180, 190, 210, 220, 230]
x = 120

def binarySearch(x, L):
    """Input: L is a sorted list of integers, x is an integer    
       Return True if x is in L, otherwise returns False"""
    low = 0
    high = len(L) - 1
    while high != low:
        guess = (low+high)//2
        if L[guess] == x:
            print(x, "found in list")
            return True
        elif L[guess] < x:
            low = guess + 1
        else:
            high = guess - 1
    return False
binarySearch(x, L)               
   
#def search(x, L):
#    count = 0
#    for elem in L:
#        count += 1
#        if elem == x:
#            print(count)
#            return True            
#        
#search(x, L)