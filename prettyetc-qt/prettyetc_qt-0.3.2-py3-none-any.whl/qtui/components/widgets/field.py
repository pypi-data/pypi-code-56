# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/field.ui',
# licensing of '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/field.ui' applies.
#
# Created: Thu Sep 12 22:13:10 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_field(object):
    def setupUi(self, field):
        field.setObjectName("field")
        field.resize(555, 46)
        field.setWindowTitle("field")
        field.setStyleSheet("")
        self.layout = QtWidgets.QHBoxLayout(field)
        self.layout.setObjectName("layout")
        self.datalayout = QtWidgets.QFormLayout()
        self.datalayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.datalayout.setObjectName("datalayout")
        self.name = QtWidgets.QLineEdit(field)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setObjectName("name")
        self.datalayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.name)
        self.data = QtWidgets.QTextEdit(field)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data.sizePolicy().hasHeightForWidth())
        self.data.setSizePolicy(sizePolicy)
        self.data.setStyleSheet("")
        self.data.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.data.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.data.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.data.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.data.setReadOnly(False)
        self.data.setAcceptRichText(True)
        self.data.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.data.setObjectName("data")
        self.datalayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.data)
        self.layout.addLayout(self.datalayout)
        self.plus = QtWidgets.QToolButton(field)
        self.plus.setObjectName("plus")
        self.layout.addWidget(self.plus)
        self.minus = QtWidgets.QToolButton(field)
        self.minus.setObjectName("minus")
        self.layout.addWidget(self.minus)
        self.layout.setStretch(0, 5)
        self.layout.setStretch(1, 1)
        self.layout.setStretch(2, 1)

        self.retranslateUi(field)
        QtCore.QMetaObject.connectSlotsByName(field)

    def retranslateUi(self, field):
        self.plus.setText(QtWidgets.QApplication.translate("field", "+", None, -1))
        self.minus.setText(QtWidgets.QApplication.translate("field", "-", None, -1))

