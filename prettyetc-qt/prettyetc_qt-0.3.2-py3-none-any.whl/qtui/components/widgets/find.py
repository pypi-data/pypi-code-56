# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/find.ui',
# licensing of '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/find.ui' applies.
#
# Created: Thu Oct 24 20:43:54 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_findAction(object):
    def setupUi(self, findAction):
        findAction.setObjectName("findAction")
        findAction.resize(480, 32)
        self.horizontalLayout = QtWidgets.QHBoxLayout(findAction)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.findtype = QtWidgets.QComboBox(findAction)
        self.findtype.setObjectName("findtype")
        self.findtype.addItem("")
        self.findtype.addItem("")
        self.findtype.addItem("")
        self.findtype.addItem("")
        self.horizontalLayout.addWidget(self.findtype)
        self.text = QtWidgets.QLineEdit(findAction)
        self.text.setText("")
        self.text.setObjectName("text")
        self.horizontalLayout.addWidget(self.text)
        self.find = QtWidgets.QToolButton(findAction)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("."), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.find.setIcon(icon)
        self.find.setObjectName("find")
        self.horizontalLayout.addWidget(self.find)

        self.retranslateUi(findAction)
        QtCore.QMetaObject.connectSlotsByName(findAction)

    def retranslateUi(self, findAction):
        findAction.setWindowTitle(QtWidgets.QApplication.translate("findAction", "Form", None, -1))
        self.findtype.setItemText(0, QtWidgets.QApplication.translate("findAction", "All", None, -1))
        self.findtype.setItemText(1, QtWidgets.QApplication.translate("findAction", "Name", None, -1))
        self.findtype.setItemText(2, QtWidgets.QApplication.translate("findAction", "Data", None, -1))
        self.findtype.setItemText(3, QtWidgets.QApplication.translate("findAction", "Description", None, -1))
        self.find.setText(QtWidgets.QApplication.translate("findAction", "...", None, -1))

