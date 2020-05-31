import sys
import logging
from os import system, chdir
from os.path import join, dirname, isdir, isfile, basename
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir
from PyQt5.Qt import QCursor
from PyQt5.QtWidgets import QWidget, QApplication, QToolBar, QMessageBox, QAction
from PyQt5.QtGui import QIcon
from .fileutil import get_file_realpath
from . import bookmark
from string import Template
from . import kdconfig

logger = logging.getLogger(__name__)


class Toolbar:

    def initToolbar(self):
        self.iconPathPrefix = "data/"
        self.actions = [{"cnName": "添加到收藏夹", "icon": "list-add.png", "action": "addBookmark"},
                        {"cnName": "从收藏夹中移除", "icon": "list-remove.png",
                            "action": "deleteBookmark"},
                        {"cnName": "主页", "icon": "go-home.png", "action": "goHome"},
                        {"cnName": "设备", "icon": "device.png",
                            "action": "initDriver"},
                        {"cnName": "收藏夹", "icon": "bookmark-book.png",
                         "action": "initBookmark"},
                        {"cnName": "终端", "icon": "terminal.png",
                            "action": "openTeminal"},
                        {"cnName": "显示文件夹", "icon": "folder.png",
                         "action": "toggleDirOnly"},
                        {"cnName": "显示隐藏文件", "icon": "eye.png",
                         "action": "toggleHiddenFile"},
                        {"cnName": "我的电脑", "icon": "computer.ico",
                         "action": "openNativeFIleManager"},
                        {"cnName": "紧凑视图", "icon": "view-list-icons.png",
                         "action": "openTeminal"},
                        {"cnName": "详细视图", "icon": "view-list-details.png",
                         "action": "openTeminal"},
                        {"cnName": "返回上级", "icon": "go-up.png",
                         "action": "goUp"},
                        {"cnName": "菜单", "icon": "menu.png", "action": "openMainMenu"}]
        self._initToolbarAction()
        self.showHiddenFileFlag = False

    def _initToolbarAction(self):
        for item in self.actions:
            self._addAction(self.iconPathPrefix +
                            item["icon"], item["cnName"], item["action"])

    def _addAction(self, iconPath, text, handler):
        action = QAction(QIcon(get_file_realpath(iconPath)), text, self)
        action.triggered.connect(getattr(self, handler))
        self.toolBar.addAction(action)

    def openTeminal(self):
        chdir(self.le_path.text())
        if self.osType:
            startfile("cmd.exe")
        else:
            system('x-terminal-emulator')

    def openNativeFIleManager(self):
        if self.osType:
            logger.info("explorer.exe '{}'".format(self.le_path.text()))
            try:
                startfile(self.le_path.text())
            except Exception as e:
                logger.error(str(e))
        else:
            system('xdg-open ' + self.le_path.text())

    def openMainMenu(self):
        action = self.main_menu.exec_(
            self.toolbar_menu.menu_item, QCursor.pos())
        if action:
            self.toolbar_menu.handle_action(action)

    def addBookmark(self):
        kdconfig.list_add("global", "bookmark", self.le_path.text())
        self.addSidebarItem(self.le_path.text())

    def deleteBookmark(self):
        item = self.lwSidebar.currentItem()
        path = item.data(-1)
        logger.info("删除收藏夹：{}".format(path))
        kdconfig.list_del("global", "bookmark", path)
        self.bookmark_list.discard(path)
        self.lwSidebar.takeItem(self.lwSidebar.currentRow())

