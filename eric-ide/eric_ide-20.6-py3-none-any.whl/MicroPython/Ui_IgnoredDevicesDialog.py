# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/MicroPython/IgnoredDevicesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IgnoredDevicesDialog(object):
    def setupUi(self, IgnoredDevicesDialog):
        IgnoredDevicesDialog.setObjectName("IgnoredDevicesDialog")
        IgnoredDevicesDialog.resize(500, 350)
        IgnoredDevicesDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(IgnoredDevicesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.devicesEditWidget = E5StringListEditWidget(IgnoredDevicesDialog)
        self.devicesEditWidget.setObjectName("devicesEditWidget")
        self.verticalLayout.addWidget(self.devicesEditWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(IgnoredDevicesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(IgnoredDevicesDialog)
        self.buttonBox.accepted.connect(IgnoredDevicesDialog.accept)
        self.buttonBox.rejected.connect(IgnoredDevicesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IgnoredDevicesDialog)

    def retranslateUi(self, IgnoredDevicesDialog):
        _translate = QtCore.QCoreApplication.translate
        IgnoredDevicesDialog.setWindowTitle(_translate("IgnoredDevicesDialog", "Ignored Serial Devices"))
from E5Gui.E5StringListEditWidget import E5StringListEditWidget
