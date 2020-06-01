# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 13:40:56 2020

@author: Aditya Vashista (101703039,TIET)
"""

import pandas as pd
import sys

def missing(arg):
    if(len(arg)!=2):
        print("Enter the cmd statement in correct syntax i.e: python missing.py <InputDataFile>")
    else:
        dataset = pd.read_csv(sys.argv[1]) #read csv file
        d= pd.DataFrame(dataset)
        for i in d: #replacing missing values with median of that column
            if d[i].dtype=='float64' or d[i].dtype=='int64':
                d[i]=d[i].fillna(d[i].median())
        d.to_csv("output.csv", index=False)
        print("Missing vales are replaced and stored in new file: output.csv")
 
missing(sys.argv)

