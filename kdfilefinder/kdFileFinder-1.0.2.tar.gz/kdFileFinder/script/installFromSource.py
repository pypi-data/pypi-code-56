'''
安装python包到系统脚本
Created on 2019年3月26日

@author: bkd
'''

from os import chdir, system
from os.path import exists, join
import logging

logger = logging.getLogger(__name__)


class installFromSource:
    def execute(self, app, sp):
        if exists(join(sp["path"], "setup.py")):
            chdir(sp["path"])
            system("python3 setup.py install --user")
            logger.info("安装python包到系统成功：" + sp["path"])
            app.statusbar.showMessage("安装python包到系统成功：" + sp["path"])
