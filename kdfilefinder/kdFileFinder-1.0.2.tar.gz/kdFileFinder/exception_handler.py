'''
Created on 2019年4月8日

@author: bkd
'''
from traceback import format_exception
import sys
import logging
from PyQt5.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


class global_exception_hander:
    def new_except_hook(self, etype, evalue, tb):
        logger.error(''.join(format_exception(etype, evalue, tb)))
        QMessageBox.information(None,
                                str('error'),
                                ''.join(format_exception(etype, evalue, tb)))
        sys.exit()

#     注册全局异常处理类
    def patch_excepthook(self):
        sys.excepthook = self.new_except_hook
