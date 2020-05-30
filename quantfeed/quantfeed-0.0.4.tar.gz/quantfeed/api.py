import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from functools import partial

default_data_host = ''

def set_default_data_host(host):
    r"""
    设定默认的数据中心地址
    """
    global default_data_host
    default_data_host = host

def get_future_contract(date_or_flag='lasest', data_host=''):
    """
    获取期货合约.
    Parameters
    ----------
        date_or_flag (str): 指定日期(格式:yyyyMMdd) 或 (lasest | all).
            lasest: 最新的上市合约.
            all: 所有的合约.
        data_host (str): 数据中心地址，通过 default_data_host 设定默认的数据中心地址.      
    """
    if data_host == '':
        data_host = default_data_host
    url = 'http://{0}/quantfeed/contract/future/{1}'.format(
        data_host, date_or_flag)
    return pd.read_json(url)

def get_main_contract(date=datetime.today().strftime('%Y%m%d'), data_host=''):
    """
    获取期货主力合约.
    Parameters
    ----------
        date (str): 指定日期(格式:yyyyMMdd), 默认值是当日
        data_host (str): 数据中心地址，通过 default_data_host 设定默认的数据中心地址.      
    """
    if data_host == '':
        data_host = default_data_host
    url = 'http://{0}/quantfeed/contract/main/{1}'.format(data_host, date)
    return pd.read_json(url)    

def __is_main(symbol):
    m = re.match('([a-zA-Z]+)(\d+)', symbol)
    if m and m.group(2) in ['88', '888', '99']:
        return (True, m.group(1), m.group(2))
    return (False, '', '')

def __parse_date(date_str, default_value):
    if re.match('\d{8}', date_str):
        return datetime.strptime(date_str, "%Y%m%d")
    return default_value

def __date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def __get_future_tick_(symbol, date, data_host):
    url = 'http://{0}/quantfeed/tick/{1}/{2}'.format(data_host, symbol, date)
    return pd.read_csv(url, header=0, engine='c')

def __add_price_adjust(series, v):
    return series + v

def __div_price_adjust(series, v):
    return series * v

def __main_info_range(product, mtype, start_date, end_date, data_host):
    url = 'http://{0}/quantfeed/main/{1}/{2}/{3}'.format(
        data_host, product, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))
    df = pd.read_json(url)
    result = []
    if mtype == '88':
        df.apply(lambda row: result.append((row['symbol'], row['date'], row['addFactor'])), axis = 1)
        result = [(item[0], item[1], partial(__add_price_adjust, v=item[2])) for item in result]
    elif mtype == '888':
        df.apply(lambda row: result.append((row['symbol'], row['date'], row['divFactor'])), axis = 1)
        result = [(item[0], item[1], partial(__div_price_adjust, v=item[2])) for item in result]
    else:
        df.apply(lambda row: result.append((row['symbol'], row['date'], lambda x: x)), axis = 1)
    return result

def __tick_info_range(symbol, start_date, end_date, data_host):
    (is_main, product, mtype) = __is_main(symbol)
    if is_main:
        return __main_info_range(product, mtype, start_date, end_date, data_host)
    return map(lambda date: (symbol, date.strftime('%Y%m%d'), lambda x: x), __date_range(start_date, end_date))

def get_future_tick(symbol, start_date, end_date, data_host=''):
    r"""
    获取期货tick数据
    Parameters
    ----------
        symbol (str): 合约名称，xx88,xx888,xx99 支持这三种连续合约.
            连续合约说明: https://gitlab.quantbox.cn/openquant/qa/blob/master/88_888_99%E8%BF%9E%E7%BB%AD%E5%90%88%E7%BA%A6.md
        start_date (str): 日期字符串(格式:yyyyMMdd), 默认是当日.
        end_date (str): 日期字符串(格式:yyyyMMdd).
        data_host (str): 数据中心地址，通过 default_data_host 设定默认的数据中心地址.
    """
    if data_host == '':
        data_host = default_data_host
    start_date = __parse_date(start_date, datetime.today())
    end_date = __parse_date(end_date, datetime.today()) + timedelta(1)
    result = pd.DataFrame()
    for (instrument, date, price_adjust) in __tick_info_range(symbol, start_date, end_date, data_host):
        tmp = __get_future_tick_(instrument, date, data_host)
        if tmp.shape[0] > 0:
            tmp['price'] = price_adjust(tmp['price'])
            tmp['ask'] = price_adjust(tmp['ask'])
            tmp['bid'] = price_adjust(tmp['bid'])
            result = result.append(tmp)
    return result
        
def get_future_bar(symbol, start_date, end_date, size=1, mode='compress', data_host=''):
    r"""
    获取期货 bar 数据
    Parameters
    ----------
        symbol (str): 合约名称，xx88,xx888,xx99 支持这三种连续合约.
            连续合约说明: https://gitlab.quantbox.cn/openquant/qa/blob/master/88_888_99%E8%BF%9E%E7%BB%AD%E5%90%88%E7%BA%A6.md
        start_date (str): 日期字符串(格式:yyyyMMdd), 默认是当日.
        end_date (str): 日期字符串(格式:yyyyMMdd).
        size (int): bar size, 单位是分钟，1,3,5 表示一分钟、三分钟和五分钟，最大值是 1440 = 日线.
        mode (str): (compress | merge) bar 生成模式，系统提供一分钟的 bar, 大于1分钟的 bar 按指定模式生成.
            compress: 按时间压缩,可能包含非交易时间例如: 30分钟 bar 会包含 10:15 - 10:30.
            merge: 按个数压缩, 例如: 30分钟 bar 是30个一分钟 bar.
        data_host (str): 数据中心地址，通过 default_data_host 设定默认的数据中心地址.
    """
    if data_host == '':
        data_host = default_data_host
    start_date = __parse_date(start_date, datetime.today()).strftime('%Y%m%d')
    end_date = __parse_date(end_date, datetime.today()).strftime('%Y%m%d')
    url = 'http://{0}/quantfeed/min/{1}/{2}/{3}/{4}/{5}'.format(
        data_host, symbol, start_date, end_date, size, mode)
    return pd.read_csv(url, header=0, engine='c')

def get_realtime_tick(symbol, data_host=''):
    r"""
    获取实时tick数据
    Parameters
    ----------
        symbol (str): 合约名称.
        data_host (str): 数据中心地址，通过 default_data_host 设定默认的数据中心地址.    
    """
    if data_host == '':
        data_host = default_data_host
    url = 'http://{0}/quantfeed/today/tick/{1}'.format(data_host, symbol)
    return pd.read_csv(url, header=0, engine='c')  

def get_realtime_min(symbol, data_host=''):
    r"""
    获取实时一分钟bar数据
    Parameters
    ----------
        symbol (str): 合约名称.
        data_host (str): 数据中心地址，通过 default_data_host 设定默认的数据中心地址.    
    """
    if data_host == '':
        data_host = default_data_host
    url = 'http://{0}/quantfeed/today/min/{1}'.format(data_host, symbol)
    return pd.read_csv(url, header=0, engine='c')  