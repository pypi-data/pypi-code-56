import sys
import uuid
import logging
import subprocess
from os.path import join, dirname, isdir, isfile, basename, expanduser, getsize
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget, QApplication, QToolBar, QMessageBox, QAction, QListView, QFileSystemModel, QStackedWidget, QTableView, QPushButton, QAbstractItemView
from PyQt5.QtGui import QIcon

logger = logging.getLogger(__name__)


class Center:

    def initCenter(self):
        self.fileSystemModelList = {}
        self.taBody.setMovable(True)
        self.taBody.setTabsClosable(True)
        self.taBody.setToolTipDuration(3000)
        self.taBody.tabCloseRequested.connect(
            lambda index: self.taBody.removeTab(index))
        self.addTab(expanduser("~"))
        self.dirOnlyFlag = False
        self.hiddenFileFlag = True

    def addTab(self, path):
        # 设置文件系统
        objectId = str(uuid.uuid4())
        logger.info("objectId：" + objectId)
        logger.info("path：" + path)
        listWidget = QListView()
        listWidget.setObjectName(objectId)
        listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.fileSystemModelList[objectId] = QFileSystemModel(listWidget)
        self.fileSystemModelList[objectId].setReadOnly(True)
        root = self.fileSystemModelList[objectId].setRootPath(path)

        # 设置视图
        listWidget.setModel(self.fileSystemModelList[objectId])

        # 绑定事假
        listWidget.clicked.connect(self.lvClickedHandler)
        listWidget.doubleClicked.connect(self.lvDoubleCilckedHandler)

        listWidget.setWrapping(True)
        listWidget.setWordWrap(True)

        # 设置过滤
        self.fileFilter = self.fileSystemModelList[objectId].filter()
        self.fileFilter_hidden = None
        self.taBody.addTab(listWidget, basename(path))
        self.taBody.setCurrentWidget(listWidget)
        self.showDir(path)

    def toggleViewMode(self, viewMode):
        rootPath = self.fileSystemModelList[objectId].rootPath()
        self.root = self.fileSystemModelList[objectId].setRootPath(rootPath)
        if 1 == viewMode:
            listWidget.setRootIndex(self.root)
            self.setCurrentWidget(listWidget)
        else:
            self.tableWidget.setRootIndex(self.root)
            self.setCurrentWidget(self.tableWidget)

    def showDir(self, itemData):
        listWidget = self.taBody.currentWidget()
        objectId = listWidget.objectName()
        logger.info("get objectId:" + objectId)
        root = self.fileSystemModelList[objectId].setRootPath(
            itemData)
        listWidget.setRootIndex(root)
        self.le_path.setText(itemData)
        self.taBody.setTabToolTip(self.taBody.currentIndex(), itemData)
        self.taBody.setTabText(
            self.taBody.currentIndex(), basename(itemData))

    # 切换状态：显示隐藏文件
    def toggleHiddenFile(self):
        listWidget = self.taBody.currentWidget()
        objectId = listWidget.objectName()
        if self.hiddenFileFlag:
            self.fileSystemModelList[objectId].setFilter(
                QDir.Hidden | QDir.Dirs | QDir.Files | QDir.NoDot | QDir.NoDotDot)
            self.hiddenFileFlag = False
        else:
            self.fileSystemModelList[objectId].setFilter(
                QDir.Dirs | QDir.Files | QDir.NoDot | QDir.NoDotDot)
            self.hiddenFileFlag = True

    # 切换状态：只显示文件夹
    def toggleDirOnly(self):
        listWidget = self.taBody.currentWidget()
        objectId = listWidget.objectName()
        if self.dirOnlyFlag:
            self.fileSystemModelList[objectId].setFilter(
                QDir.Dirs | QDir.Files | QDir.NoDot | QDir.NoDotDot)
            self.dirOnlyFlag = False
        else:
            self.fileSystemModelList[objectId].setFilter(
                QDir.Dirs | QDir.NoDot | QDir.NoDotDot)
            self.dirOnlyFlag = True
            # self.fileSystemModelList[objectId].setFilter(self.fileFilter)

    def focusInEvent(self, event):
        logger.info("获得焦点")
        logger.info("输入焦点在", self.id)
        QStackedWidget.focusInEvent(self, e)

    def lvDoubleCilckedHandler(self):
        listWidget = self.taBody.currentWidget()
        objectId = listWidget.objectName()
        cur_item_index = listWidget.currentIndex()
        cur_item = self.fileSystemModelList[objectId].itemData(
            cur_item_index)[0]
        fileName = join(
            self.le_path.text(), cur_item)
        logger.info("双击打开文件:" + fileName)
        if isfile(str(fileName)):
            subprocess.call(["xdg-open", fileName])

    def lvClickedHandler(self):
        listWidget = self.taBody.currentWidget()
        objectId = listWidget.objectName()
        logger.info("get objectId:" + objectId)
        cur_item_index = listWidget.currentIndex()
        cur_item1 = self.fileSystemModelList[objectId].itemData(
            cur_item_index)
        cur_item = cur_item1[0]
        logger.info("cur_item", cur_item1)
        sub_path = join(
            self.fileSystemModelList[objectId].rootPath(), cur_item)
        logger.info("sub_path:" + sub_path)
        if isdir(str(sub_path)):
            logger.info(sub_path + "is a dir")
            # self.le_path.setText(sub_path)
            # self.on_pb_load_path_clicked()
            # self.showDir(sub_path)
            #self.setAddressSignal.emit(sub_path, self)
            self.showDir(sub_path)
        elif isfile(str(sub_path)):
            logger.info(sub_path + " is a file")
            self.statusbar.showMessage("{}({})".format(
                cur_item, self.sizeFormat(getsize(sub_path))))
            #subprocess.call(["xdg-open", sub_path])
        else:
            logger.info(type(sub_path))

    def sizeFormat(self, size):
        if size < 1000:
            return '%i' % size + 'kb'
        elif 1000 <= size < 1000000:
            return '%.1f' % float(size / 1000) + 'KB'
        elif 1000000 <= size < 1000000000:
            return '%.1f' % float(size / 1000000) + 'MB'
        elif 1000000000 <= size < 1000000000000:
            return '%.1f' % float(size / 1000000000) + 'GB'
        elif 1000000000000 <= size:
            return '%.1f' % float(size / 1000000000000) + 'TB'
    # 返回上级

    def goUp(self):
        parent_dir = dirname(self.le_path.text())
        if parent_dir == self.le_path.text() and self.isWindowsOS or parent_dir == "/":
            # windows系统的分区的根目录无上级根目录
            pass
        else:
            self.showDir(parent_dir)

    def goHome(self):
        self.showDir(QDir.home().absolutePath())

    @pyqtSlot()
    def on_le_path_returnPressed(self):
        self.showDir(self.le_path.text())
