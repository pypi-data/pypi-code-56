'''
Created on 2019年3月26日

@author: bkd

复制文件的完整路径
'''
from PyQt5.QtWidgets import QApplication
from os.path import join
import logging

logger = logging.getLogger(__name__)


class copyFilepath:
    def execute(self, app, sp):
        filePath = join(sp["path"], sp["fileList"][0])
        clipboard = QApplication.clipboard()
        clipboard.setText(filePath)
        logger.info("已复制文件路径：" + filePath)
        app.statusbar.showMessage("已复制文件路径：" + filePath)
