# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/mainwindow.ui',
# licensing of '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/mainwindow.ui' applies.
#
# Created: Fri Nov  1 12:00:06 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 606)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.root = QtWidgets.QWidget(MainWindow)
        self.root.setAutoFillBackground(False)
        self.root.setObjectName("root")
        self.rootLayout = QtWidgets.QGridLayout(self.root)
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.rootLayout.setObjectName("rootLayout")
        self.configs_tabs = QtWidgets.QTabWidget(self.root)
        self.configs_tabs.setStyleSheet("QTabWidget{\n"
"    border: 2px solid transparent;\n"
"}\n"
"")
        self.configs_tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.configs_tabs.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.configs_tabs.setTabsClosable(True)
        self.configs_tabs.setMovable(True)
        self.configs_tabs.setObjectName("configs_tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.configs_tabs.addTab(self.tab, "")
        self.rootLayout.addWidget(self.configs_tabs, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.root)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 30))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menu_settings = QtWidgets.QMenu(self.menubar)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_info = QtWidgets.QMenu(self.menubar)
        self.menu_info.setObjectName("menu_info")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar = QtWidgets.QToolBar(MainWindow)
        self.toolbar.setMovable(True)
        self.toolbar.setObjectName("toolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.action_new = QtWidgets.QAction(MainWindow)
        self.action_new.setObjectName("action_new")
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_saveas = QtWidgets.QAction(MainWindow)
        self.action_saveas.setObjectName("action_saveas")
        self.action_preferences = QtWidgets.QAction(MainWindow)
        self.action_preferences.setObjectName("action_preferences")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menufile.addAction(self.action_new)
        self.menufile.addAction(self.action_open)
        self.menufile.addAction(self.action_save)
        self.menufile.addAction(self.action_saveas)
        self.menu_settings.addAction(self.action_preferences)
        self.menu_info.addAction(self.action_about)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menu_info.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.toolbar.addAction(self.action_new)
        self.toolbar.addAction(self.action_open)
        self.toolbar.addAction(self.action_save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_preferences)
        self.toolbar.addSeparator()

        self.retranslateUi(MainWindow)
        self.configs_tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.action_open, QtCore.SIGNAL("triggered()"), MainWindow.open_confile)
        QtCore.QObject.connect(self.action_preferences, QtCore.SIGNAL("triggered()"), MainWindow.open_settings)
        QtCore.QObject.connect(self.action_about, QtCore.SIGNAL("triggered()"), MainWindow.open_about)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Prettyetc", None, -1))
        self.configs_tabs.setTabText(self.configs_tabs.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "Page", None, -1))
        self.menufile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menu_settings.setTitle(QtWidgets.QApplication.translate("MainWindow", "Options", None, -1))
        self.menu_info.setTitle(QtWidgets.QApplication.translate("MainWindow", "Info", None, -1))
        self.toolbar.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.action_new.setText(QtWidgets.QApplication.translate("MainWindow", "New", None, -1))
        self.action_new.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+N", None, -1))
        self.action_open.setText(QtWidgets.QApplication.translate("MainWindow", "Open", None, -1))
        self.action_open.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+O", None, -1))
        self.action_save.setText(QtWidgets.QApplication.translate("MainWindow", "Save", None, -1))
        self.action_save.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+S", None, -1))
        self.action_saveas.setText(QtWidgets.QApplication.translate("MainWindow", "Save as", None, -1))
        self.action_saveas.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, -1))
        self.action_preferences.setText(QtWidgets.QApplication.translate("MainWindow", "Preferences", None, -1))
        self.action_about.setText(QtWidgets.QApplication.translate("MainWindow", "About", None, -1))

from . import logo_rc
