import pandas as pd
import numpy as np
import time
import datetime
import math
import csv, json
import os
from sense_hat import SenseHat
sense = SenseHat()

def datadisplay():
    path1 = "THP_Sensing"
    path2 = "THP_Sensing/Raw_data"
    path3 = "THP_Sensing/Avg"
    path4 = "THP_Sensing/Avg/Avg_Raw_data(All)"
    path5 = "THP_Sensing/Avg/Avg(1min)"
    path6 = "THP_Sensing/Avg/Avg(10min)"
    path7 = "THP_Sensing/Avg/Avg(1hr)"
    path8 = "THP_Sensing/Avg/Avg(24hrs)"
    path9 = "THP_Sensing/Avg/Avg(48hrs)"
    path10 = "THP_Sensing/Json"
    
    os.mkdir(path1); os.mkdir(path2); os.mkdir(path3); os.mkdir(path4); os.mkdir(path5); os.mkdir(path6); os.mkdir(path7); os.mkdir(path8); os.mkdir(path9); os.mkdir(path10)
    print(format("Date" "        Time" "       Temp(C)" "  Press(hPa)" "  Humid(%)"))
    filename = datetime.datetime.now().strftime("THP_Sensing/Raw_data/%Y-%m-%d  %H:%M:%S.csv")
    avgfilename = datetime.datetime.now().strftime("THP_Sensing/Avg/Avg_Raw_data(All)/avg(%Y-%m-%d  %H:%M:%S).csv")
    while True:
        t = sense.get_temperature()
        p = sense.get_pressure()
        h = sense.get_humidity()
        
        print(format("%s,  %.2f,   %.2f,     %.0f" % (datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"), t, p, h)))
        myFile=open(filename, 'a')
        myFile.write("%s,  %.2f,   %.2f,     %.0f\n" % (datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"), t, p, h))
        myFile.close()
        time.sleep(1 - time.time() % 1)
        
        df = pd.read_csv(filename, names=['Date Time','Temp(C)','Press(hPa)','Humid(%)'])
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

        df1.tail(100).to_csv('THP_Sensing/Avg/Avg(1min)/avgTHP1min.csv')
        df2.tail(100).to_csv('THP_Sensing/Avg/Avg(10min)/avgTHP10min.csv')
        df3.tail(100).to_csv('THP_Sensing/Avg/Avg(1hr)/avgTHP1hr.csv')
        df4.tail(100).to_csv('THP_Sensing/Avg/Avg(24hrs)/avgTHP24hrs.csv')
        df5.tail(100).to_csv('THP_Sensing/Avg/Avg(48hrs)/avgTHP48hrs.csv')
        
        dff.to_csv(avgfilename)
        dff.tail(100).to_csv('THP_Sensing/Avg/avgTHPAll.csv')
        
        csvFilepath = "THP_Sensing/Avg/avgTHPAll.csv"
        jsonFilepath = "THP_Sensing/Json/avgTHPAll.json"

        data = {}
        with open(csvFilepath) as csvFile:
            csvReader = csv.DictReader(csvFile)
            for csvRow in csvReader:
                sl_no = csvRow['Sl No.']
                data[sl_no] = csvRow

        with open('THP_Sensing/Json/avgTHPAll.json', 'w') as jsonFile:
            jsonFile.write(json.dumps(data, indent=4))
              