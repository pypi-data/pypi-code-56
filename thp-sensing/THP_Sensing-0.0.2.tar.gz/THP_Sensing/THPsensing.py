import time
import datetime
import math
from DataMgmt import datamgmt
from Jsondata import jsondata
from sense_hat import SenseHat
sense = SenseHat()

def display():
    print(format("Date" "        Time" "       Temp(C)" "  Press(hPa)" "  Humid(%)"))
    filename = datetime.datetime.now().strftime("Raw_data/%Y-%m-%d  %H:%M:%S.csv")
    avgfilename = datetime.datetime.now().strftime("Avg/Avg_Raw_data(All)/avg(%Y-%m-%d  %H:%M:%S).csv")
    while True:
        t = sense.get_temperature()
        p = sense.get_pressure()
        h = sense.get_humidity()
        
        print(format("%s,  %.2f,   %.2f,     %.0f" % (datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"), t, p, h)))
        myFile=open(filename, 'a')
        myFile.write("%s,  %.2f,   %.2f,     %.0f\n" % (datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"), t, p, h))
        myFile.close()
        time.sleep(1 - time.time()%1)
        
        datamgmt(filename,avgfilename)
        
        jsondata()
        
        
        
    
        
