from math import asin, cos, sqrt

def lnglat2str(lon1, lat1, lon2, lat2):
    p = 0.017453292519943295  # Math.PI / 180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + \
          cos(lat1 * p) * cos(lat2 * p) * \
          (1 - cos((lon2 - lon1) * p))/2 
    return 12742000 * asin(sqrt(a))