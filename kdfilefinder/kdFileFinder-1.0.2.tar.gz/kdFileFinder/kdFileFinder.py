#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Created on 2019年3月7日

@author: bkd
'''

import sys
import subprocess
import logging
from os.path import join, dirname, isdir, isfile, basename
from os import system, chdir
from PyQt5.Qt import QCursor, QAbstractItemView
try:
    from os import startfile
except Exception as e:
    pass
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QDir, Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileSystemModel, QAction, QListWidgetItem, QMenu, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from .fileutil import get_file_realpath
from . import kdconfig
from .exception_handler import global_exception_hander
from .scriptManager import ScriptManager
from .sidebar import Sidebar
from .toolbar import Toolbar
from .center import Center
from .kdFileFinder_ui import Ui_kdFileFinder
from PyQt5.QtWidgets import QWidget, QApplication, QToolBar, QMessageBox, QAction, QListView, QFileSystemModel, QStackedWidget, QTableView
from os.path import join, dirname, isdir, isfile, basename, expanduser


logger = logging.getLogger(__name__)


class kdFileFinder(QMainWindow, Ui_kdFileFinder, Sidebar, Center, Toolbar, ScriptManager):

    def __init__(self):
        # UI初始化
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(get_file_realpath('data/kdFileFinder.png')))
        self.showMaximized()

        # 系统变量初始化
        self.osType = sys.platform == "win32"
        self.last_open_file = set()

        # 界面组件初始化
        self.initToolbar()
        self.initSidebar()
        self.initCenter()
        self.initScriptManager()

        # 拦截系统异常
        self.exception_handler = global_exception_hander()
        self.exception_handler.patch_excepthook()

        # 系统菜单初始化
        # self.main_menu = QMenu()
        self.file_menu = QMenu()
        # self.folder_menu = QMenu()
        # self.toolbar_menu = toolbar_menu()
        # self.file_popup_menu = file_menu()

        # self.ScriptManager = ScriptManager()
        self.taBody.installEventFilter(self)

    def eventFilter(self, qobject, qevent):
        qtype = qevent.type()
        if qtype == 82:
            listWidget = self.taBody.currentWidget()
            counter = len(listWidget.selectedIndexes())

            # 右键所在的位置又可能是空白处
            if counter == 1:
                logger.info("单选")
                i = listWidget.indexAt(QCursor.pos())
                if not i.isValid():
                    logger.info("单选选中")
                    # self.goUp()
                    # counter = len(listWidget.selectedIndexes())
                else:
                    logger.info("单选未选中")

#             处理选中的文件
            if counter >= 1:
                logger.info("弹出右键菜单")
                action = self.file_menu.exec_(
                    self.get_file_menu_item(), QCursor.pos())
                if action:
                    listWidget = self.taBody.currentWidget()
                    objectId = listWidget.objectName()
                    file_list = [self.fileSystemModelList[objectId].itemData(
                        i)[0] for i in listWidget.selectedIndexes()]
                    logger.info("执行右键指定的脚本：" + action.text())
                    self.run_script(
                        action.text(), self.le_path.text(), file_list)
#             选中空白处，返回上层目录
            else:
                self.goUp()
        return False

#     拦截快捷键
    def keyPressEvent(self, event):
        key = event.key()
        logger.info("按下：" + str(event.key()))
        modifer = event.modifiers()
        if modifer == Qt.ControlModifier:
            self.ctrlKeyHandler(key)

    def ctrlKeyHandler(self, key):
        if key == Qt.Key_T:
            self.addTab(self.le_path.text())
        elif key == Qt.Key_W:
            self.taBody.removeTab(self.taBody.currentIndex())
        elif key == Qt.Key_Q:
            sys.exit(0)
        elif key == Qt.Key_C:
            listWidget = self.taBody.currentWidget()
            objectId = listWidget.objectName()
            file_list = [self.fileSystemModelList[objectId].itemData(
                i)[0] for i in listWidget.selectedIndexes()]
            self.run_script("复制", self.le_path.text(), file_list)
        elif key == Qt.Key_V:
            self.run_script("粘贴", self.le_path.text(), None)
            # if  key == Qt.Key_C:
            # file_list = [self.fileSystemModel.itemData(
            # i)[0] for i in self.center.selectedIndexes()]
            # self.ScriptManager.run_script(
            # "复制", self.le_path.text(), file_list)
        # elif event.modifiers() == Qt.ControlModifier and key == Qt.Key_V:
            # self.ScriptManager.run_script("粘贴", self.le_path.text(), None)
        # elif key == Qt.Key_F2:
            # file_list = [self.fileSystemModel.itemData(
            # self.center.currentIndex())[0]]
            # self.ScriptManager.run_script(
            # "重命名", self.le_path.text(), file_list)
        # elif event.modifiers() == Qt.ControlModifier and key == Qt.Key_D:
            # self.lb_sidebar.setText("收藏夹")
            # self.sidebar.add_sidebar_item(self.le_path.text())
            # kdconfig.list_add("global", "bookmark", self.le_path.text())
        # elif event.modifiers() == Qt.ControlModifier and key == Qt.Key_T:
            # self.lb_sidebar.setText("标签")
            # self.sidebar.add_sidebar_item(self.le_path.text())
        # elif event.modifiers() == Qt.ControlModifier and key == None:
            # self.center.setSelectionMode(
            # QAbstractItemView.ExtendedSelection)
            # logger.info("duoxuan")
        # elif event.modifiers() == Qt.ShiftModifier and key == None:
            # self.center.setSelectionMode(
            # QAbstractItemView.ContiguousSelection)
            # logger.info("shit 多选")
        # elif event.modifiers() == Qt.ControlModifier and key == Qt.Key_T:
            # self.addTab(self.le_path.text())
#     def keyReleaseEvent(self, event):
#         key = event.key()
#         logger.info("按下：" + str(event.key()))
#         if key == Qt.Key_Control:
#             self.center.setSelectionMode(QAbstractItemView.SingleSelection)
#             logger.info("danxuan")


def main():
    app = QApplication(sys.argv)
    win = kdFileFinder()
    win.show()
    sys.exit(app.exec_())
