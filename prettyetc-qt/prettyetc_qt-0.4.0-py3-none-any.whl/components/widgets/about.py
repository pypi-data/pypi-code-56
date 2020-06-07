# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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

from  . import logo_rc

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(616, 528)
        self.verticalLayout = QVBoxLayout(About)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, -1, 0)
        self.label_logo = QLabel(About)
        self.label_logo.setObjectName(u"label_logo")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setMaximumSize(QSize(64, 64))
        self.label_logo.setSizeIncrement(QSize(0, 0))
        self.label_logo.setPixmap(QPixmap(u":/images/logo.png"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_logo)

        self.verticalWidget = QWidget(About)
        self.verticalWidget.setObjectName(u"verticalWidget")
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.verticalWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.title_label = QLabel(self.verticalWidget)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_5.addWidget(self.title_label)


        self.horizontalLayout.addWidget(self.verticalWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(About)
        self.tabWidget.setObjectName(u"tabWidget")
        self.info_tab = QWidget()
        self.info_tab.setObjectName(u"info_tab")
        self.verticalLayout_2 = QVBoxLayout(self.info_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.info_label = QLabel(self.info_tab)
        self.info_label.setObjectName(u"info_label")
        self.info_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.info_label)

        self.tabWidget.addTab(self.info_tab, "")
        self.lib_tab = QWidget()
        self.lib_tab.setObjectName(u"lib_tab")
        self.verticalLayout_3 = QVBoxLayout(self.lib_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lib_label = QLabel(self.lib_tab)
        self.lib_label.setObjectName(u"lib_label")
        self.lib_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.lib_label)

        self.tabWidget.addTab(self.lib_tab, "")
        self.authors_tab = QWidget()
        self.authors_tab.setObjectName(u"authors_tab")
        self.verticalLayout_4 = QVBoxLayout(self.authors_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.authors_label = QLabel(self.authors_tab)
        self.authors_label.setObjectName(u"authors_label")
        self.authors_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.authors_label.setOpenExternalLinks(True)

        self.verticalLayout_4.addWidget(self.authors_label)

        self.tabWidget.addTab(self.authors_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(About)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(About)
        self.buttonBox.accepted.connect(About.accept)
        self.buttonBox.rejected.connect(About.reject)

        self.tabWidget.setCurrentIndex(1)

    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"About", None))
        self.label_logo.setText("")
        self.title_label.setText(QCoreApplication.translate("About", u"PRETTYETC", None))
        self.info_label.setText(QCoreApplication.translate("About", u"<html><head/><body><p>Browse your configuration files in a visual way with a pretty and universal interface.<br/></p><p>Copyright 2019, trollodel</p><p>Prettyetc UI $prettyetc_ui</p><p>Prettyetc Core library $prettyetc.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.info_tab), QCoreApplication.translate("About", u"About", None))
        self.lib_label.setText(QCoreApplication.translate("About", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">GUI:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://www.qt.io/\"><span style=\" text-decoration: underline; color:#007af4;\">QT Framework $qt</span></a></li>\n"
"<li style=\"\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://wiki.qt.io/Qt_for_Python\"><"
                        "span style=\" text-decoration: underline; color:#007af4;\">PySide2 binding for QT Framework $pyside2</span></a></li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">CORE:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/dwavesystems/homebase\"><span style=\" text-decoration: underline; color:#007af4;\">homebase $homebase</span></a></li></ul>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/lark-parser/lark\"><span style=\" text-decoration: underline; color:#007af4;\">lark-parser"
                        " $lark</span></a></li>\n"
"<li style=\"\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://sourceforge.net/projects/ruamel-yaml/\"><span style=\" text-decoration: underline; color:#007af4;\">ruamel.yaml $ruamel</span></a></li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lib_tab), QCoreApplication.translate("About", u"Libraries", None))
        self.authors_label.setText(QCoreApplication.translate("About", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Main developers</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">trollodel (<a href=\"https://gitlab.com/trollodel\"><span style=\" text-decoration: underline; color:#007af4;\">Gitlab</span></a>) </li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Contributors</p>\n"
"<ul style=\""
                        "margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Cattai Lorenzo (<a href=\"https://gitlab.com/cattai_lorenzo\"><span style=\" text-decoration: underline; color:#007af4;\">Gitlab</span></a>) </li></ul>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Christian (<a href=\"https://gitlab.com/Chris1101x\"><span style=\" text-decoration: underline; color:#007af4;\">Gitlab</span></a>) </li></ul></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.authors_tab), QCoreApplication.translate("About", u"Authors", None))
    # retranslateUi

