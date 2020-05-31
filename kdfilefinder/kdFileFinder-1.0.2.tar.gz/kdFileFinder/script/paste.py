'''
粘贴脚本
Created on 2019年3月26日

@author: bkd
'''
import logging
from shutil import copy2, copytree, rmtree, move
from os.path import basename, join, exists, isfile, isdir
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QGuiApplication

logger = logging.getLogger(__name__)


class paste(QMessageBox):
    def execute(self, app, sp):
        self.pasteType = sp["pasteType"]
        pastePath = sp["pastePath"]
        fileList = sp["pasteFileList"]
        destPath = sp["path"]

        # clipboard = QGuiApplication.clipboard()
        # mimeData = clipboard.mimeData()
        # if not mimeData.hasFormat("text/uri-list"):
        # logger.info("剪切板为空")
        # return

        # urls = mimeData.urls()

        for file in fileList:
            src = join(pastePath, file)
            dst = join(destPath, file)
            is_exists = exists(dst)
            if isfile(src):
                self.handleFile(is_exists, src, dst)
            elif isdir(src):
                self.handleDir(is_exists, src, dst)
            else:
                logger.info("无法复制的项目")

    def handleFile(self, is_exists, src, dst):
        if is_exists:
            reply = self.information(
                self, "确认文件替换", "该位置已存在一个同名的文件" + basename(src), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                logger.info("目标文件已存在")
                self.handleFileByPasteType(src, dst)
        else:
            self.handleFileByPasteType(src, dst)

    def handleFileByPasteType(self, src, dst):
        if self.pasteType == "cut":
            logger.info("移动文件：" + src + "->" + dst)
            move(src, dst)
        else:
            logger.info("复制文件：" + src + "->" + dst)
            copy2(src, dst)

    def handleDirByPasteType(self, src, dst):
        if self.pasteType == "cut":
            logger.info("移动文件：" + src + "->" + dst)
            move(src, dst)
        else:
            logger.info("复制文件夹：" + src + "->" + dst)
            copytree(src, dst)

    def handleDir(self, is_exists, src, dst):
        if is_exists:
            reply = self.information(
                self, "确认文件夹替换", "该位置已存在一个同名的文件夹" + basename(src), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                logger.info("删除已存在的目标文件夹：" + dst)
                rmtree(dst)
                logger.info("复制文件夹：" + src + "->" + dst)
                self.handleDirByPasteType(src, dst)
        else:
            logger.info("复制文件夹：" + src + "->" + dst)
            self.handleDirByPasteType(src, dst)
