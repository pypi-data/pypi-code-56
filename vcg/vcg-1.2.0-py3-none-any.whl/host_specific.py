# -*- coding: utf-8 -*-
# @Time    : 2020/6/6 16:04
# @Author  : Yinglin Zheng
# @Email   : zhengyinglin@stu.xmu.edu.cn
# @File    : host_specific.py
# @Software: PyCharm
# @Affiliation: VCG@XMU

import socket
from .tools import load_json


class HostSpecific:
    def __init__(self, obj, fallback="default"):
        if isinstance(obj, str):
            items = load_json(obj)
        else:
            items = obj
        computer_name = socket.gethostname()
        if computer_name in items:
            self._items = items[computer_name]
        else:
            self._items = items[fallback]
        self.computer_name = computer_name

    def __getitem__(self, item):
        return self._items[item]

    def __str__(self):
        return str(self._items)

    def __getattr__(self, item):
        return self._items[item]
