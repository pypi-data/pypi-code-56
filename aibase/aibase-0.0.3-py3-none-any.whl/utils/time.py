# -*- coding: utf-8 -*-
# @Time: 2020/6/3 0003
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:

import datetime
import time

DEFAULE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def current_time(format=DEFAULE_DATE_FORMAT):
    """
        获取指定格式的时间字符串
    :param format: 时间格式
    :return: 指定格式的时间字符串
    """
    return datetime.datetime.now().strftime(format)


def current_timestamp(ms=True):
    """
        获取当前时间时间戳
    :param ms: 是否包含毫秒
    :return:
    """
    if ms:
        return int(time.time() * 1000)
    else:
        return int(time.time())


__all__ = ['current_time', 'current_timestamp']

if __name__ == '__main__':
    print(current_time())
    print(current_time(format='%Y%m%d%H%M%S'))
    print(datetime.datetime.now())
    print(datetime.date.today())
    print(current_timestamp())
    print(int(time.time() * 1000))
