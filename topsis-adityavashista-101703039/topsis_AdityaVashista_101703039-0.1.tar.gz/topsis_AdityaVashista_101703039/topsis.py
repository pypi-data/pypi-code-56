# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 23:27:12 2020

@author: Aditya Vashista (101703039,TIET)
"""
import sys
import pandas as pd

def topsis(arg):
    if(len(arg)!=4):
        print("Enter the cmd statement in correct syntax i.e: python topsis.py <InputDataFile> <Weights> <Impacts>")
    else:
        if(isinstance(arg[-1], str) and isinstance(arg[-2], str)):
            if(len((arg[-1]).split(","))!=len((arg[-2]).split(","))):
               print("Number of weights and impacts shold be same")
            elif(all(x in ["+","-"] for x in (arg[-1]).split(","))):
                dataset = pd.read_csv(arg[1]) #read csv file
                x=dataset.iloc[:,1:].values #get recquired data
                y=len(x)#number of rows
                
                weights=arg[2] #read weights
                w=weights.split(",") #list of string
                n=len(w) #number of columns 
                
                #finding denominator for standardization
                std=[]
                for i in range(n):
                    sum=0
                    for j in range(y):
                        sum+=(x[j][i])**2
                    std.append(float(format(sum**0.5,'.4f')))
                
                #modifying table enteries   
                M = [[0.0000 for i in range(n)] for j in range(y)] 
                for i in range(y):
                    for j in range(n):
                        a=float(x[i][j])
                        a=float(format((a/std[j]),'.4f'))
                        M[i][j]=a*float(w[j])
                
                impacts=arg[3] #read impacts
                imp=impacts.split(",")
                
                ib=[]#ideal best
                iw=[]#ideal worst
                for i in range(n):#loop to iw and ib of each column
                    l=[row[i] for row in M]
                    if imp[i]=="-":
                        ib.append(min(l))
                        iw.append(max(l))
                    else:
                        ib.append(max(l))
                        iw.append(min(l))
                
                #calculate performance        
                performance=[]
                for i in range(y):
                    sb=0
                    sw=0
                    for j in range(n):
                        sb+=float(format((M[i][j]-ib[j])**2,'.4f'))
                        sw+=float(format((M[i][j]-iw[j])**2,'.4f'))
                    sb=sb**0.5
                    sw=sw**0.5
                    p=sw/(sb+sw)
                    performance.append(p)
                
                #finding best option
                best=performance.index(max(performance))
                print("best option: "+dataset.iloc[best,0])
            else:
                print("Impacts must be in +/- only")
        else:
            print("Weights and Impacts must be passed as single string")

arg=sys.argv
topsis(arg)
