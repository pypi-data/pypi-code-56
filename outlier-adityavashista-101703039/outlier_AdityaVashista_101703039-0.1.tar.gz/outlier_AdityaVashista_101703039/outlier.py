# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:13:32 2020

@author:  Aditya Vashista (101703039,TIET)
"""
import pandas as pd
import sys

#defining fuction to store valid rows into new file using IQR
def IQR(data):
    q1 =data.quantile(0.25)
    q3 = data.quantile(0.75)
    IQR = q3-q1
    dataNew = data[~((data < (q1 - (1.5 * IQR))) |(data> (q3 + 1.5 * IQR))).any(axis=1)]
    dataNew.to_csv("output.csv", index=False)
    return len(dataNew)
#Outlier detection function
def outlier(filename):
	d =pd.read_csv(filename)
	x = d.iloc[:,:-1]
	data= pd.DataFrame(x)
	rowsValid=0
	rowsValid=IQR(data)
	print("Number of outliers/rows removed = "+ str(len(data)-rowsValid))

    
#Execution
outlier(sys.argv[1])


