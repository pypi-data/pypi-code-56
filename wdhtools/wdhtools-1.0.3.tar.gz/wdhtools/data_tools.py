#!/usr/bin/env python
# coding: utf-8

# @Author: dehong
# @Date: 2020-06-05
# @Time: 10:38
# @Name: data_tools
import pandas as pd

"""
1. isnull 空缺值查看 
2. fillna 空缺值填充
3. deletes 删除多个特征 
"""


def isnull(data):
    """
    查看当前数据中哪些特征含有空值,以及空值的数量
    :param data: DataFrame | 操作数据集
    :return: 包含空值的数据
    """
    value_data = pd.DataFrame(data.isnull().sum(), columns=['value'])
    null_data = value_data[value_data['value'] > 0]
    null_data.sort_values(by='value', ascending=False, inplace=True)
    return null_data


def fillna(data, features, how='zero', custom=0):
    """
    缺失值填充, 支持 'zero'(0),'null'(null字符串),'mean'(平均数),'mode'(众数),'custom'(自定义custom值) 填充
    :param data:
    :param features:
    :param how:
    :param custom:
    :return:
    """
    for feature in features:
        if how == 'zero':
            data[feature].fillna(0, inplace=True)
        elif how == 'null':
            data[feature].fillna("null", inplace=True)
        elif how == 'mean':
            mean = data[feature].mean()
            data[feature].fillna(mean, inplace=True)
        elif how == 'mode':
            mode = data[feature].mode()
            data[feature].filna(mode, inplace=True)
        elif how == 'custom':
            data[feature].fillna(custom, inplace=True)
        else:
            print("非法填充方式！！！仅支持 'zero','null','mean','mode','self' 填充")
    return data


def deletes(data, features):
    """
    删除指定特征
    :param data: DataFrame | 操作数据集
    :param features: list | 需要删除的特征列表
    :return: DataFrame
    """
    for feature in features:
        del data[feature]
    print("当前删除特征:", features)
    return data


data = pd.read_csv('/Users/fotoable/Desktop/4.csv')
print(isnull(data))