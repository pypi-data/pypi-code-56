'''
Created on 2019年3月26日

@author: bkd

复制文件名
'''
from PyQt5.QtWidgets import QApplication
import logging

logger = logging.getLogger(__name__)


class copyFilename:
    def execute(self, app, sp):
        fileName = sp["fileList"][0]
        clipboard = QApplication.clipboard()
        clipboard.setText(fileName)
        logger.info("已复制文件名：" + fileName)
        app.statusbar.showMessage("已复制文件名：" + fileName)
