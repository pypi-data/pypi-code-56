# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logViewWindowTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExport = QtWidgets.QMenu(self.menubar)
        self.menuExport.setObjectName("menuExport")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/open-folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad.setIcon(icon)
        self.actionLoad.setObjectName("actionLoad")
        self.actionPlots_pdf = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/load_bw.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlots_pdf.setIcon(icon1)
        self.actionPlots_pdf.setObjectName("actionPlots_pdf")
        self.actionData_csv = QtWidgets.QAction(MainWindow)
        self.actionData_csv.setIcon(icon1)
        self.actionData_csv.setObjectName("actionData_csv")
        self.menuFile.addAction(self.actionLoad)
        self.menuExport.addSeparator()
        self.menuExport.addAction(self.actionPlots_pdf)
        self.menuExport.addAction(self.actionData_csv)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())

        self.retranslateUi(MainWindow)
        self.actionLoad.triggered.connect(MainWindow.load_file)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "Open"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.actionLoad.setText(_translate("MainWindow", "File"))
        self.actionPlots_pdf.setText(_translate("MainWindow", "Plots (pdf)"))
        self.actionData_csv.setText(_translate("MainWindow", "Data (csv)"))
import resource_kamzik3_rc
