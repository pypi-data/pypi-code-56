'''
Created on 2019年3月26日

@author: bkd
'''

from os import chdir, system
from os.path import exists, join


class buildSourceDistribute:
    def execute(self, app, sp):
        if exists(join(sp["path"], "setup.py")):
            chdir(sp["path"])
            system("python3 setup.py sdist")
