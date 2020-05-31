'''
重命名脚本
Created on 2019年4月8日

@author: bkd
'''
from os.path import join
from os import rename as osRename
from PyQt5.QtWidgets import QInputDialog
import logging

logger = logging.getLogger(__name__)


class rename:
    def execute(self, app, sp):
        originName = sp["fileList"][0]
        curPath = sp["path"]
        filePath = join(curPath, originName)
        new_name, ok = QInputDialog.getText(None, "重命名文件", "请输入一个新名称：")
        if ok and new_name != originName:
            osRename(filePath, join(curPath, new_name))
            logger.info("重命名文件：" + filePath + "->" + join(curPath, new_name))
            app.statusbar.showMessage(
                "重命名文件：" + filePath + "->" + join(curPath, new_name))
