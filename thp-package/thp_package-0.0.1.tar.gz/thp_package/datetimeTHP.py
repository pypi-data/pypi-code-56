import time
import datetime
import math
from DataMgmnt import datamgmnt
from Jsondata import jsondata
from sense_hat import SenseHat
sense = SenseHat()

print(format("Date" "        Time" "       Temp(C)" "  Press(hPa)" "  Humid(%)"))
filename = datetime.datetime.now().strftime("Date_Time data/%Y-%m-%d  %H:%M:%S.csv")
while True:
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()
    
    print(format("%s,  %.2f,   %.2f,     %.0f" % (datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"), t, p, h)))
    myFile=open(filename, 'a')
    myFile.write("%s,  %.2f,   %.2f,     %.0f\n" % (datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"), t, p, h))
    myFile.close()
    time.sleep(1 - time.time() % 1)
    
    datamgmnt(filename)
    
    jsondata()
    
    
        
