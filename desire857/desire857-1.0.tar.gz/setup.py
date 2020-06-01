# -*- coding utf-8 -*-
# @Time    : 2020/6/1 21:45
# @Author  : DesireYang
# @Email   : yangyin1106@163.com
# @File    : setup.py
# Software : PyCharm
# Explain  : 

from distutils.core import setup

setup(
    name='desire857',  # 对外模块的名字
    version='1.0',  # 版本号
    description='接口自动化模块，用于测试哦',  # 描述
    author='yang857',  # 作者
    author_email='yangyin1106@163.com',
    py_modules=['desire857.common.Yaml_Handle', 'desire857.common.Logging_Handle', 'desire857.common.Request_Handle']  # 要发布的模块
)
