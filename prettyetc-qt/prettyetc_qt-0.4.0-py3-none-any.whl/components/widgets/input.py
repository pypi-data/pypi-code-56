# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_inputdialog(object):
    def setupUi(self, inputdialog):
        if not inputdialog.objectName():
            inputdialog.setObjectName(u"inputdialog")
        inputdialog.resize(399, 108)
        self.layout = QVBoxLayout(inputdialog)
        self.layout.setObjectName(u"layout")
        self.inputlabel = QLabel(inputdialog)
        self.inputlabel.setObjectName(u"inputlabel")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputlabel.sizePolicy().hasHeightForWidth())
        self.inputlabel.setSizePolicy(sizePolicy)

        self.layout.addWidget(self.inputlabel)

        self.inputwid = QLineEdit(inputdialog)
        self.inputwid.setObjectName(u"inputwid")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.inputwid.sizePolicy().hasHeightForWidth())
        self.inputwid.setSizePolicy(sizePolicy1)

        self.layout.addWidget(self.inputwid)

        self.buttonbox = QDialogButtonBox(inputdialog)
        self.buttonbox.setObjectName(u"buttonbox")
        sizePolicy1.setHeightForWidth(self.buttonbox.sizePolicy().hasHeightForWidth())
        self.buttonbox.setSizePolicy(sizePolicy1)
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.layout.addWidget(self.buttonbox)

#if QT_CONFIG(shortcut)
        self.inputlabel.setBuddy(self.inputwid)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(inputdialog)
    # setupUi

    def retranslateUi(self, inputdialog):
        inputdialog.setWindowTitle(QCoreApplication.translate("inputdialog", u"Dialog", None))
        self.inputlabel.setText(QCoreApplication.translate("inputdialog", u"TextLabel", None))
    # retranslateUi

