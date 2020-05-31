'''
解压到当前目录脚本

Created on 2019年3月27日

@author: bkd
'''
from shutil import unpack_archive
from os.path import join
import logging
logger = logging.getLogger(__name__)


class unpackHere:
    def execute(self, app, sp):
        for file in sp['fileList']:
            filePath = join(sp["path"], file)
            unpack_archive(filePath, extract_dir=sp["path"])
            logger.info("解压文件成功：" + file)
            app.statusbar.showMessage("解压文件成功：" + file)
