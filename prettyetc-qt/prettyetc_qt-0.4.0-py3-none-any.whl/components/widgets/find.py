# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'find.ui'
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


class Ui_findAction(object):
    def setupUi(self, findAction):
        if not findAction.objectName():
            findAction.setObjectName(u"findAction")
        findAction.resize(480, 32)
        self.horizontalLayout = QHBoxLayout(findAction)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.findtype = QComboBox(findAction)
        self.findtype.addItem("")
        self.findtype.addItem("")
        self.findtype.addItem("")
        self.findtype.addItem("")
        self.findtype.setObjectName(u"findtype")

        self.horizontalLayout.addWidget(self.findtype)

        self.text = QLineEdit(findAction)
        self.text.setObjectName(u"text")

        self.horizontalLayout.addWidget(self.text)

        self.find = QToolButton(findAction)
        self.find.setObjectName(u"find")
        icon = QIcon()
        iconThemeName = u"find"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.find.setIcon(icon)

        self.horizontalLayout.addWidget(self.find)


        self.retranslateUi(findAction)
    # setupUi

    def retranslateUi(self, findAction):
        findAction.setWindowTitle(QCoreApplication.translate("findAction", u"Form", None))
        self.findtype.setItemText(0, QCoreApplication.translate("findAction", u"All", None))
        self.findtype.setItemText(1, QCoreApplication.translate("findAction", u"Name", None))
        self.findtype.setItemText(2, QCoreApplication.translate("findAction", u"Data", None))
        self.findtype.setItemText(3, QCoreApplication.translate("findAction", u"Description", None))

        self.text.setText("")
        self.find.setText(QCoreApplication.translate("findAction", u"...", None))
    # retranslateUi

