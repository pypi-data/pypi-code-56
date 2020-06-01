# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 11:00
# @Author  : Desire
# @Email   : yangyin1106@163.com
# @Blog    : https://www.cnblogs.com/desireyang/
# @File    : Request_Handle.py
# @Software: PyCharm
import requests
from requests import Response


def send_requests(url, method, params=None, json=None, data=None, headers=None) -> Response:
    """
    发送http请求
    :param url: 请求地址
    :param method: 请求方式
    :param params: get请求参数
    :param json: json请求参数
    :param data: x-www-form-urlencoded格式数据
    :param headers: 请求头
    :return: 响应结果
    """
    # 将大写转化成小写
    method = method.lower()
    methods = {
        'get': requests.get,
        'post': requests.post,
        'patch': requests.patch
    }
    if method in methods:
        return methods[method](url=url, params=params, json=json, data=data, headers=headers)
    else:
        raise ValueError("请求方式输入有误")
