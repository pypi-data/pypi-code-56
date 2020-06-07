# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(740, 606)
        icon = QIcon()
        icon.addFile(u":/images/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        icon1 = QIcon()
        iconThemeName = u"document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_new.setIcon(icon1)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        icon2 = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_open.setIcon(icon2)
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        icon3 = QIcon()
        iconThemeName = u"document-save"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_save.setIcon(icon3)
        self.action_saveas = QAction(MainWindow)
        self.action_saveas.setObjectName(u"action_saveas")
        self.action_saveas.setIcon(icon3)
        self.action_preferences = QAction(MainWindow)
        self.action_preferences.setObjectName(u"action_preferences")
        icon4 = QIcon()
        iconThemeName = u"preferences"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_preferences.setIcon(icon4)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        icon5 = QIcon()
        iconThemeName = u"about"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u":/images/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_about.setIcon(icon5)
        self.action_add = QAction(MainWindow)
        self.action_add.setObjectName(u"action_add")
        icon6 = QIcon()
        iconThemeName = u"add"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_add.setIcon(icon6)
        font = QFont()
        font.setPointSize(16)
        self.action_add.setFont(font)
        self.action_delete = QAction(MainWindow)
        self.action_delete.setObjectName(u"action_delete")
        icon7 = QIcon()
        iconThemeName = u"delete"
        if QIcon.hasThemeIcon(iconThemeName):
            icon7 = QIcon.fromTheme(iconThemeName)
        else:
            icon7.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_delete.setIcon(icon7)
        self.root = QWidget(MainWindow)
        self.root.setObjectName(u"root")
        self.root.setAutoFillBackground(False)
        self.rootLayout = QGridLayout(self.root)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget(self.root)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setStyleSheet(u"QTabWidget{\n"
"	border: 2px solid transparent;\n"
"}\n"
"")
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabShape(QTabWidget.Triangular)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.dummy_tab = QWidget()
        self.dummy_tab.setObjectName(u"dummy_tab")
        self.dummy_tab.setLayoutDirection(Qt.LeftToRight)
        self.tabs.addTab(self.dummy_tab, "")

        self.rootLayout.addWidget(self.tabs, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.root)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 740, 23))
        self.menubar.setNativeMenuBar(True)
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_settings = QMenu(self.menubar)
        self.menu_settings.setObjectName(u"menu_settings")
        self.menu_info = QMenu(self.menubar)
        self.menu_info.setObjectName(u"menu_info")
        self.menu_edit = QMenu(self.menubar)
        self.menu_edit.setObjectName(u"menu_edit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar_general = QToolBar(MainWindow)
        self.toolbar_general.setObjectName(u"toolbar_general")
        self.toolbar_general.setEnabled(True)
        self.toolbar_general.setMovable(True)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolbar_general)
        self.toolbar_edit = QToolBar(MainWindow)
        self.toolbar_edit.setObjectName(u"toolbar_edit")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolbar_edit)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_info.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_settings.addAction(self.action_preferences)
        self.menu_info.addAction(self.action_about)
        self.menu_edit.addAction(self.action_add)
        self.menu_edit.addAction(self.action_delete)
        self.toolbar_general.addAction(self.action_new)
        self.toolbar_general.addAction(self.action_open)
        self.toolbar_general.addAction(self.action_save)
        self.toolbar_general.addSeparator()
        self.toolbar_general.addAction(self.action_preferences)
        self.toolbar_general.addSeparator()
        self.toolbar_edit.addAction(self.action_add)
        self.toolbar_edit.addAction(self.action_delete)

        self.retranslateUi(MainWindow)
        self.action_open.triggered.connect(MainWindow.open_confile)
        self.action_preferences.triggered.connect(MainWindow.open_settings)
        self.action_about.triggered.connect(MainWindow.open_about)
        self.action_save.triggered.connect(MainWindow.save)
        self.action_saveas.triggered.connect(MainWindow.open_saveas)
        self.action_new.triggered.connect(MainWindow.new)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Prettyetc", None))
        self.action_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.action_new.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.action_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.action_save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_saveas.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
#if QT_CONFIG(shortcut)
        self.action_saveas.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_preferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
#if QT_CONFIG(tooltip)
        self.action_add.setToolTip(QCoreApplication.translate("MainWindow", u"Add a new field", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_add.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+A", None))
#endif // QT_CONFIG(shortcut)
        self.action_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(tooltip)
        self.action_delete.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected fields", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_delete.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.tabs.setTabText(self.tabs.indexOf(self.dummy_tab), QCoreApplication.translate("MainWindow", u"Page", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_settings.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menu_info.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.toolbar_general.setWindowTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.toolbar_edit.setWindowTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

