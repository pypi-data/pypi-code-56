import sys
import logging
from os.path import join, dirname, isdir, isfile, basename
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QMessageBox, QListWidgetItem
from .fileutil import get_file_realpath
from . import bookmark

logger = logging.getLogger(__name__)


class Sidebar:
    def initSidebar(self):
        super().__init__()
        self.lwSidebar.itemClicked.connect(
            self.currentItemChangedHandler)

        self.bookmark_list = bookmark.get_bookmark()
        logger.debug("收藏夹：" + str(self.bookmark_list))
        self.initBookmark()
        logger.info("初始化侧边栏结束")

    def initBookmark(self):
        self.lwSidebar.clear()
        if self.bookmark_list:
            for b in self.bookmark_list:
                self.addSidebarItem(b)

    def addSidebarItem(self, path):
        item = None
        if not basename(path):
            item = QListWidgetItem(path)
        else:
            item = QListWidgetItem(basename(path))
        item.setData(-1, path)
        self.lwSidebar.addItem(item)

    def initDriver(self):
        self.lwSidebar.clear()
        if self.osType:
            drivers = QDir.drives()
            for driver in drivers:
                self.addSidebarItem(driver.absoluteFilePath())
        else:
            dirs = QDir("/").entryList(QDir.Dirs)
            for dir in dirs:
                if "." == dir or ".." == dir:
                    continue
                self.addSidebarItem("/" + dir)

    def currentItemChangedHandler(self, item):
        if item:
            self.showDir(item.data(-1))
