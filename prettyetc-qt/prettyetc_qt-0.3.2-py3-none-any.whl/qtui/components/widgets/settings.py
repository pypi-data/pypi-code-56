# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/settings.ui',
# licensing of '/home/Public/prog/python3/prettyetc/prettyetc/qtui/components/design/settings.ui' applies.
#
# Created: Fri Nov  1 17:58:32 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_settings(object):
    def setupUi(self, settings):
        settings.setObjectName("settings")
        settings.resize(626, 329)
        self.verticalLayout = QtWidgets.QVBoxLayout(settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setting_tabs = QtWidgets.QTabWidget(settings)
        self.setting_tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.setting_tabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setting_tabs.setObjectName("setting_tabs")
        self.tab_view = QtWidgets.QWidget()
        self.tab_view.setEnabled(True)
        self.tab_view.setObjectName("tab_view")
        self.formLayout_2 = QtWidgets.QFormLayout(self.tab_view)
        self.formLayout_2.setObjectName("formLayout_2")
        self.view_rootfield_label = QtWidgets.QLabel(self.tab_view)
        self.view_rootfield_label.setObjectName("view_rootfield_label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.view_rootfield_label)
        self.view_rootfield = QtWidgets.QComboBox(self.tab_view)
        self.view_rootfield.setObjectName("view_rootfield")
        self.view_rootfield.addItem("")
        self.view_rootfield.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.view_rootfield)
        self.setting_tabs.addTab(self.tab_view, "")
        self.tab_appearance = QtWidgets.QWidget()
        self.tab_appearance.setObjectName("tab_appearance")
        self.formLayout_3 = QtWidgets.QFormLayout(self.tab_appearance)
        self.formLayout_3.setObjectName("formLayout_3")
        self.appearance_theme_label = QtWidgets.QLabel(self.tab_appearance)
        self.appearance_theme_label.setObjectName("appearance_theme_label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.appearance_theme_label)
        self.appearance_theme = QtWidgets.QComboBox(self.tab_appearance)
        self.appearance_theme.setObjectName("appearance_theme")
        self.appearance_theme.addItem("")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.appearance_theme)
        self.setting_tabs.addTab(self.tab_appearance, "")
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
        self.enableFindExperimentalLabel = QtWidgets.QLabel(self.tab_debug)
        self.enableFindExperimentalLabel.setObjectName("enableFindExperimentalLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.enableFindExperimentalLabel)
        self.debug_enable_find = QtWidgets.QCheckBox(self.tab_debug)
        self.debug_enable_find.setObjectName("debug_enable_find")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.debug_enable_find)
        self.setting_tabs.addTab(self.tab_debug, "")
        self.verticalLayout.addWidget(self.setting_tabs)
        self.buttonbox = QtWidgets.QDialogButtonBox(settings)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonbox.setCenterButtons(False)
        self.buttonbox.setObjectName("buttonbox")
        self.verticalLayout.addWidget(self.buttonbox)

        self.retranslateUi(settings)
        self.setting_tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonbox, QtCore.SIGNAL("clicked(QAbstractButton*)"), settings.handle_btnbox)
        QtCore.QObject.connect(self.buttonbox, QtCore.SIGNAL("accepted()"), settings.accept)
        QtCore.QObject.connect(self.buttonbox, QtCore.SIGNAL("rejected()"), settings.reject)
        QtCore.QMetaObject.connectSlotsByName(settings)

    def retranslateUi(self, settings):
        settings.setWindowTitle(QtWidgets.QApplication.translate("settings", "Dialog", None, -1))
        self.view_rootfield_label.setText(QtWidgets.QApplication.translate("settings", "Default view for Tree", None, -1))
        self.view_rootfield.setItemText(0, QtWidgets.QApplication.translate("settings", "Source", None, -1))
        self.view_rootfield.setItemText(1, QtWidgets.QApplication.translate("settings", "Tree", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_view), QtWidgets.QApplication.translate("settings", "View", None, -1))
        self.appearance_theme_label.setText(QtWidgets.QApplication.translate("settings", "Theme", None, -1))
        self.appearance_theme.setItemText(2, QtWidgets.QApplication.translate("settings", "Default", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_appearance), QtWidgets.QApplication.translate("settings", "Appearance", None, -1))
        self.debug_hidden_actions_label.setText(QtWidgets.QApplication.translate("settings", "Enable hidden actions", None, -1))
        self.enableFindExperimentalLabel.setText(QtWidgets.QApplication.translate("settings", "Enable find (experimental)", None, -1))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_debug), QtWidgets.QApplication.translate("settings", "Debug", None, -1))

