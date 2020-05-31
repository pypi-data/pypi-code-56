'''
删除脚本
Created on 2019年3月26日

@author: bkd
'''
import os
from os.path import join, exists
from PyQt5.QtWidgets import QMessageBox, QInputDialog
import logging

logger = logging.getLogger(__name__)


class mkdir:
    def execute(self, app, sp):
        newName, ok = QInputDialog.getText(None, "新的文件夹名", "请输入一个文件夹的名称：")
        filePath = join(sp['path'], newName)
        if not ok:
            return
        if exists(filePath):
            reply = QMessageBox.information(
                app, "已存在同名文件夹", "该位置已存在一个同名的文件夹，请重新输入一个文件夹名称", QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.execute(app, sp)
        else:
            os.mkdir(filePath)
            logger.info("创建文件夹成功：" + filePath)
            app.statusbar.showMessage("创建文件夹成功：" + filePath)
