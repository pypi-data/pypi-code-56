from urllib.request import urlopen
from urllib.parse import *
import json


def lnglat2car(lng1, lat1, lng2, lat2, key="49a90a6e71c311843d5eb9ae406be79b"):
    """汽车导航

    Parameters
    ----------

    Return
    ------
    distance : float
        导航距离（米）
    duration : int
        导航时间（秒）
    """
    url="https://restapi.amap.com/v3/direction/driving?origin={},{}&destination={},{}&strategy=12&extensions=base&key={}".format(
        lng1, lat1, lng2, lat2, key)
    try:
        req = urlopen(url)
        content = req.read().decode('utf-8')
        distance = json.loads(content, encoding='gbk')['route']['paths'][0]['distance']
        duration = json.loads(content, encoding='gbk')['route']['paths'][0]['duration']
        return float(distance), float(duration)
    except Exception:
        print("{},{};{},{}获取汽车导航出现异常".format(lng1, lat1, lng2, lat2))
        return 0

