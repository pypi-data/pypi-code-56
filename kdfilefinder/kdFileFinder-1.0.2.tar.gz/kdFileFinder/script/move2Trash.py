'''
移动到回收站脚本
Created on 2020年5月31日

@author: bkd
'''
import os
from os.path import join, exists
from send2trash import send2trash
from PyQt5.QtWidgets import QMessageBox, QInputDialog
import logging

logger = logging.getLogger(__name__)


class move2Trash:
    def execute(self, app, sp):
        path = sp["path"]
        fileList = sp["fileList"]
        for file in fileList:
            filePath = join(path, file)
            send2trash(filePath)
            logger.info("移动到回收站成功：" + filePath)
            app.statusbar.showMessage("移动到回收站成功：" + filePath)
