# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/settings.ui',
# licensing of '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/settings.ui' applies.
#
# Created: Fri Aug 16 18:22:27 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_settings(object):
    def setupUi(self, settings):
        settings.setObjectName("settings")
        settings.resize(465, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setting_tabs = QtWidgets.QTabWidget(settings)
        self.setting_tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.setting_tabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setting_tabs.setObjectName("setting_tabs")
        self.tab_general = QtWidgets.QWidget()
        self.tab_general.setObjectName("tab_general")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_general)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.tab_general)
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.horizontalLayout_5.addWidget(self.textBrowser_5)
        self.setting_tabs.addTab(self.tab_general, "")
        self.tab_parsing = QtWidgets.QWidget()
        self.tab_parsing.setObjectName("tab_parsing")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_parsing)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.tab_parsing)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.horizontalLayout_4.addWidget(self.textBrowser_4)
        self.setting_tabs.addTab(self.tab_parsing, "")
        self.tab_writing = QtWidgets.QWidget()
        self.tab_writing.setObjectName("tab_writing")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_writing)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_writing)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.setting_tabs.addTab(self.tab_writing, "")
        self.tab_advanced = QtWidgets.QWidget()
        self.tab_advanced.setObjectName("tab_advanced")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_advanced)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_advanced)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_2.addWidget(self.textBrowser_2)
        self.setting_tabs.addTab(self.tab_advanced, "")
        self.tab_debug = QtWidgets.QWidget()
        self.tab_debug.setObjectName("tab_debug")
        self.formLayout = QtWidgets.QFormLayout(self.tab_debug)
        self.formLayout.setObjectName("formLayout")
        self.debug_hidden_actions_label = QtWidgets.QLabel(self.tab_debug)
        self.debug_hidden_actions_label.setObjectName("debug_hidden_actions_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.debug_hidden_actions_label)
        self.debug_hidden_actions = QtWidgets.QCheckBox(self.tab_debug)
        self.debug_hidden_actions.setObjectName("debug_hidden_actions")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.debug_hidden_actions)
        self.debug_custom_style_sheet_label = QtWidgets.QLabel(self.tab_debug)
        self.debug_custom_style_sheet_label.setObjectName("debug_custom_style_sheet_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.debug_custom_style_sheet_label)
        self.debug_custom_style_sheet = QtWidgets.QLineEdit(self.tab_debug)
        self.debug_custom_style_sheet.setObjectName("debug_custom_style_sheet")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.debug_custom_style_sheet)
        self.setting_tabs.addTab(self.tab_debug, "")
        self.verticalLayout.addWidget(self.setting_tabs)
        self.buttonBox = QtWidgets.QDialogButtonBox(settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(settings)
        self.setting_tabs.setCurrentIndex(4)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), settings.reject)
        QtCore.QMetaObject.connectSlotsByName(settings)

    def retranslateUi(self, settings):
        settings.setWindowTitle(QtWidgets.QApplication.translate("settings", "Dialog", None, -1))
        self.textBrowser_5.setHtml(QtWidgets.QApplication.translate("settings", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">Coming Soon</span></p></body></html>", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_general), QtWidgets.QApplication.translate("settings", "General", None, -1))
        self.textBrowser_4.setHtml(QtWidgets.QApplication.translate("settings", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">Coming Soon</span></p></body></html>", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_parsing), QtWidgets.QApplication.translate("settings", "Parsing", None, -1))
        self.textBrowser.setHtml(QtWidgets.QApplication.translate("settings", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">Coming Soon</span></p></body></html>", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_writing), QtWidgets.QApplication.translate("settings", "Writing", None, -1))
        self.textBrowser_2.setHtml(QtWidgets.QApplication.translate("settings", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">Coming Soon</span></p></body></html>", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_advanced), QtWidgets.QApplication.translate("settings", "Advanced", None, -1))
        self.debug_hidden_actions_label.setText(QtWidgets.QApplication.translate("settings", "Enable hidden actions", None, -1))
        self.debug_custom_style_sheet_label.setText(QtWidgets.QApplication.translate("settings", "Custom style sheet", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_debug), QtWidgets.QApplication.translate("settings", "debug", None, -1))

