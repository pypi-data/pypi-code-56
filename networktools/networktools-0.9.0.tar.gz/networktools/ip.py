import os
import random

"""
To obtain available ports
"""


def network_ip():
    command = "hostname -I"
    retvalue = os.popen(command).readlines()
    return str(retvalue[0][0:-1]).strip()
