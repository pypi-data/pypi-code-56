'''
创建txt文件脚本，默认utf-8编码
Created on 2019年3月26日

@author: bkd
'''
import os
from os.path import join, exists
from PyQt5.QtWidgets import QMessageBox, QInputDialog
import logging

logger = logging.getLogger(__name__)


class createTxt:
    def execute(self, app, sp):
        newName, ok = QInputDialog.getText(None, "新的文件名", "请输入一个文件的名称：")
        filePath = join(sp['path'], newName)
        if not ok:
            return
        if exists(filePath):
            reply = QMessageBox.information(
                app, "已存在同名文件", "该位置已存在一个同名的文件，请重新输入一个文件名称", QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.execute(app, sp)
        else:
            with open(filePath, "w+", encoding="utf-8"):
                pass
            logger.info("创建文件成功：" + filePath)
            app.statusbar.showMessage("创建文件成功：" + filePath)
