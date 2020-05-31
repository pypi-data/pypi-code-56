'''
删除脚本
Created on 2019年3月26日

@author: bkd
'''
from os import remove
from os.path import join
from shutil import rmtree
from os.path import isfile, isdir
import logging

logger = logging.getLogger(__name__)


class delete:
    def execute(self, app, sp):
        path = sp["path"]
        fileList = sp["fileList"]
        for file in fileList:
            filePath = join(path, file)
            if isfile(filePath):
                remove(filePath)
                logger.info("删除文件成功，" + filePath)
                app.statusbar.showMessage("删除文件成功，" + filePath)
            elif isdir(filePath):
                rmtree(filePath)
                logger.info("删除目录成功，" + filePath)
                app.statusbar.showMessage("删除目录成功，" + filePath)
            else:
                logger.info("无法删除的项目")
                app.statusbar.showMessage("无法删除的项目")
