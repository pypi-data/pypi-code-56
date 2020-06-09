from urllib.request import urlopen
from urllib.parse import *
import string
import json


def address2lnglat(address, ak='8De7y5MmGOy6HlPn5KZH112brsKZRvSw'):
    """通过地址获取经纬度

    Parameters
    ----------
    address ： string
        详细地址
    ak ：string
        百度开发者key
    Return
    ------
    distance : float
        导航距离（米）
    duration : int
        导航时间（秒）
    """
    url= 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}'.format(address, ak)
    url = quote(url, safe=string.printable)
    try:
        req = urlopen(url)
        content = req.read().decode('utf-8')
        print(content)
        location = json.loads(content, encoding='gbk')['result']['location']
        return location['lng'], location['lat']
    except Exception:
        print("获取{}经纬度出现异常".format(address))
        return 0, 0


def lnglat2bike(lng1, lat1, lng2, lat2, key="8De7y5MmGOy6HlPn5KZH112brsKZRvSw"):
    """自行车导航

    Parameters
    ----------

    Return
    ------
    distance : float
        导航距离（米）
    duration : int
        导航时间（秒）
    """
    url = "http://apifdidi.map.baidu.com/directionlite/v1/riding?origin={},{}&destination={},{}&ak={}&riding_type=1&coord_type=gcj02".format(lat1, lng1, lat2, lng2, key)
    try:
        req = urlopen(url)
        content = req.read().decode('utf-8')
        distance = json.loads(content, encoding='gbk')['result']['routes'][0]['distance']
        duration = json.loads(content, encoding='gbk')['result']['routes'][0]['duration']
        routes = json.loads(content, encoding='gbk')['result']['routes']
        return float(distance), float(duration), routes
    except Exception:
        print("{},{};{},{}获取自行车导航出现异常".format(lng1, lat1, lng2, lat2))
        return 0, 0, None




