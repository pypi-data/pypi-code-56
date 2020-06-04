# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:36:37 2019

@author: yuanq
"""

import socket

def get_ipv4():
    return socket.gethostbyname(socket.gethostname())

