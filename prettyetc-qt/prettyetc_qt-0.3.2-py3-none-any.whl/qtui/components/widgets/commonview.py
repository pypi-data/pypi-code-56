# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/commonview.ui',
# licensing of '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/commonview.ui' applies.
#
# Created: Fri Sep 13 21:39:36 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_fieldview(object):
    def setupUi(self, fieldview):
        fieldview.setObjectName("fieldview")
        fieldview.resize(592, 640)
        self.rootLayout = QtWidgets.QVBoxLayout(fieldview)
        self.rootLayout.setObjectName("rootLayout")
        self.widget = QtWidgets.QWidget(fieldview)
        self.widget.setObjectName("widget")
        self.navbar = QtWidgets.QHBoxLayout(self.widget)
        self.navbar.setContentsMargins(0, 0, 0, 0)
        self.navbar.setObjectName("navbar")
        self.rootLayout.addWidget(self.widget)
        self.root = QtWidgets.QWidget(fieldview)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.root.sizePolicy().hasHeightForWidth())
        self.root.setSizePolicy(sizePolicy)
        self.root.setObjectName("root")
        self.rootLayout.addWidget(self.root)

        self.retranslateUi(fieldview)
        QtCore.QMetaObject.connectSlotsByName(fieldview)

    def retranslateUi(self, fieldview):
        fieldview.setWindowTitle(QtWidgets.QApplication.translate("fieldview", "Form", None, -1))

