import pandas as pd
import numpy as np
import math
import csv

def datamgmnt(csvfile):
    df = pd.read_csv(csvfile, names=['Date Time','Temp(C)','Press(hPa)','Humid(%)'])
    first_col = df['Date Time']
    second_col = df['Temp(C)']
    third_col = df['Press(hPa)']
    fourth_col = df['Humid(%)']
    df = df.rename_axis('Sl No.')

    df = pd.DataFrame(df)

    df['avg(1min) T(C)'] = df.iloc[:,1].rolling(window=60).mean()
    df['avg(1min) P(hPa)'] = df.iloc[:,2].rolling(window=60).mean()
    df['avg(1min) H(%)'] = df.iloc[:,3].rolling(window=60).mean()

    df['avg(10min) T(C)'] = df.iloc[:,1].rolling(window=600).mean()
    df['avg(10min) P(hPa)'] = df.iloc[:,2].rolling(window=600).mean()
    df['avg(10min) H(%)'] = df.iloc[:,3].rolling(window=600).mean()

    df['avg(1hr) T(C)'] = df.iloc[:,1].rolling(window=3600).mean()
    df['avg(1hr) P(hPa)'] = df.iloc[:,2].rolling(window=3600).mean()
    df['avg(1hr) H(%)'] = df.iloc[:,3].rolling(window=3600).mean()

    df['avg(24hrs) T(C)'] = df.iloc[:,1].rolling(window=86400).mean()
    df['avg(24hrs) P(hPa)'] = df.iloc[:,2].rolling(window=86400).mean()
    df['avg(24hrs) H(%)'] = df.iloc[:,3].rolling(window=86400).mean()
  
    df['avg(48hrs) T(C)'] = df.iloc[:,1].rolling(window=172800).mean()
    df['avg(48hrs) P(hPa)'] = df.iloc[:,2].rolling(window=172800).mean()
    df['avg(48hrs) H(%)'] = df.iloc[:,3].rolling(window=172800).mean()
    
    dff = df.round(2)
    
    df1 = dff.drop(['Temp(C)','Press(hPa)','Humid(%)','avg(10min) T(C)','avg(10min) P(hPa)','avg(10min) H(%)','avg(1hr) T(C)','avg(1hr) P(hPa)','avg(1hr) H(%)','avg(24hrs) T(C)','avg(24hrs) P(hPa)','avg(24hrs) H(%)','avg(48hrs) T(C)','avg(48hrs) P(hPa)','avg(48hrs) H(%)'], axis=1)
    df2 = dff.drop(['Temp(C)','Press(hPa)','Humid(%)','avg(1min) T(C)','avg(1min) P(hPa)','avg(1min) H(%)','avg(1hr) T(C)','avg(1hr) P(hPa)','avg(1hr) H(%)','avg(24hrs) T(C)','avg(24hrs) P(hPa)','avg(24hrs) H(%)','avg(48hrs) T(C)','avg(48hrs) P(hPa)','avg(48hrs) H(%)'], axis=1)
    df3 = dff.drop(['Temp(C)','Press(hPa)','Humid(%)','avg(10min) T(C)','avg(10min) P(hPa)','avg(10min) H(%)','avg(1min) T(C)','avg(1min) P(hPa)','avg(1min) H(%)','avg(24hrs) T(C)','avg(24hrs) P(hPa)','avg(24hrs) H(%)','avg(48hrs) T(C)','avg(48hrs) P(hPa)','avg(48hrs) H(%)'], axis=1)
    df4 = dff.drop(['Temp(C)','Press(hPa)','Humid(%)','avg(10min) T(C)','avg(10min) P(hPa)','avg(10min) H(%)','avg(1hr) T(C)','avg(1hr) P(hPa)','avg(1hr) H(%)','avg(1min) T(C)','avg(1min) P(hPa)','avg(1min) H(%)','avg(48hrs) T(C)','avg(48hrs) P(hPa)','avg(48hrs) H(%)'], axis=1)
    df5 = dff.drop(['Temp(C)','Press(hPa)','Humid(%)','avg(10min) T(C)','avg(10min) P(hPa)','avg(10min) H(%)','avg(1hr) T(C)','avg(1hr) P(hPa)','avg(1hr) H(%)','avg(24hrs) T(C)','avg(24hrs) P(hPa)','avg(24hrs) H(%)','avg(1min) T(C)','avg(1min) P(hPa)','avg(1min) H(%)'], axis=1)

    df1.tail(100).to_csv('Avg/Avg(1min)/avgTHP1min.csv')
    df2.tail(100).to_csv('Avg/Avg(10min)/avgTHP10min.csv')
    df3.tail(100).to_csv('Avg/Avg(1hr)/avgTHP1hr.csv')
    df4.tail(100).to_csv('Avg/Avg(24hrs)/avgTHP24hrs.csv')
    df5.tail(100).to_csv('Avg/Avg(48hrs)/avgTHP48hrs.csv')
    
    dff.to_csv('Avg/AvgRawData/avgrawdata.csv')
    dff.tail(100).to_csv('Avg/avgTHPAll.csv')
    