#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by MonNet on 2020/5/31
# File    : base.py
import random

def generate_random_phone():
    '''
    生成随机手机号
    :return:
    '''
    prefix = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                 "141", "145", "146", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159","166",
                 "170", "172", "173", "174", "176", "177", "178", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189",
                 "198", "199"]
    return random.choice(prefix)+"".join(random.choice("0123456789") for i in range(8))