'''
Created on 2019年3月26日

@author: bkd
'''
try:
    from os import startfile
except Exception as e:
    pass
from sys import platform
from os import system
from os.path import join
import subprocess


class open:
    def execute(self, app, sp):
        for fileName in sp['fileList']:
            filePath = join(sp['path'], fileName)
            if platform == "win32":
                startfile(filePath)
            else:
                subprocess.call(["xdg-open", filePath])
