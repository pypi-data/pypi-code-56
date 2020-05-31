# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bkd/pyqt/kdFileFinder/kdFileFinder/kdFileFinder.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_kdFileFinder(object):
    def setupUi(self, kdFileFinder):
        kdFileFinder.setObjectName("kdFileFinder")
        kdFileFinder.resize(646, 583)
        self.centralwidget = QtWidgets.QWidget(kdFileFinder)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lwSidebar = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lwSidebar.sizePolicy().hasHeightForWidth())
        self.lwSidebar.setSizePolicy(sizePolicy)
        self.lwSidebar.setObjectName("lwSidebar")
        self.gridLayout.addWidget(self.lwSidebar, 1, 0, 1, 1)
        self.le_path = QtWidgets.QLineEdit(self.centralwidget)
        self.le_path.setObjectName("le_path")
        self.gridLayout.addWidget(self.le_path, 0, 0, 1, 3)
        self.taBody = QtWidgets.QTabWidget(self.centralwidget)
        self.taBody.setObjectName("taBody")
        self.gridLayout.addWidget(self.taBody, 1, 1, 1, 1)
        kdFileFinder.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(kdFileFinder)
        self.statusbar.setObjectName("statusbar")
        kdFileFinder.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(kdFileFinder)
        self.toolBar.setObjectName("toolBar")
        kdFileFinder.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(kdFileFinder)
        self.taBody.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(kdFileFinder)

    def retranslateUi(self, kdFileFinder):
        _translate = QtCore.QCoreApplication.translate
        kdFileFinder.setWindowTitle(_translate("kdFileFinder", "kdFileFinder"))
        self.le_path.setText(_translate("kdFileFinder", "/tmp"))
        self.toolBar.setWindowTitle(_translate("kdFileFinder", "toolBar"))
