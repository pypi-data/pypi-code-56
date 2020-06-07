# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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


class Ui_settings(object):
    def setupUi(self, settings):
        if not settings.objectName():
            settings.setObjectName(u"settings")
        settings.resize(626, 329)
        self.verticalLayout = QVBoxLayout(settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.setting_tabs = QTabWidget(settings)
        self.setting_tabs.setObjectName(u"setting_tabs")
        self.setting_tabs.setTabPosition(QTabWidget.North)
        self.setting_tabs.setTabShape(QTabWidget.Rounded)
        self.tab_view = QWidget()
        self.tab_view.setObjectName(u"tab_view")
        self.tab_view.setEnabled(True)
        self.formLayout_2 = QFormLayout(self.tab_view)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.view_rootfield_label = QLabel(self.tab_view)
        self.view_rootfield_label.setObjectName(u"view_rootfield_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.view_rootfield_label)

        self.view_rootfield = QComboBox(self.tab_view)
        self.view_rootfield.addItem("")
        self.view_rootfield.addItem("")
        self.view_rootfield.setObjectName(u"view_rootfield")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.view_rootfield)

        self.setting_tabs.addTab(self.tab_view, "")
        self.tab_appearance = QWidget()
        self.tab_appearance.setObjectName(u"tab_appearance")
        self.formLayout_3 = QFormLayout(self.tab_appearance)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.appearance_theme_label = QLabel(self.tab_appearance)
        self.appearance_theme_label.setObjectName(u"appearance_theme_label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.appearance_theme_label)

        self.appearance_theme = QComboBox(self.tab_appearance)
        self.appearance_theme.addItem("")
        self.appearance_theme.setObjectName(u"appearance_theme")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.appearance_theme)

        self.setting_tabs.addTab(self.tab_appearance, "")
        self.tab_debug = QWidget()
        self.tab_debug.setObjectName(u"tab_debug")
        self.formLayout = QFormLayout(self.tab_debug)
        self.formLayout.setObjectName(u"formLayout")
        self.enableFindExperimentalLabel = QLabel(self.tab_debug)
        self.enableFindExperimentalLabel.setObjectName(u"enableFindExperimentalLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.enableFindExperimentalLabel)

        self.debug_enable_find = QCheckBox(self.tab_debug)
        self.debug_enable_find.setObjectName(u"debug_enable_find")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.debug_enable_find)

        self.setting_tabs.addTab(self.tab_debug, "")

        self.verticalLayout.addWidget(self.setting_tabs)

        self.buttonbox = QDialogButtonBox(settings)
        self.buttonbox.setObjectName(u"buttonbox")
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)
        self.buttonbox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonbox)

#if QT_CONFIG(shortcut)
        self.view_rootfield_label.setBuddy(self.view_rootfield)
        self.appearance_theme_label.setBuddy(self.appearance_theme)
        self.enableFindExperimentalLabel.setBuddy(self.debug_enable_find)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(settings)
        self.buttonbox.clicked.connect(settings.handle_btnbox)
        self.buttonbox.accepted.connect(settings.accept)
        self.buttonbox.rejected.connect(settings.reject)

        self.setting_tabs.setCurrentIndex(0)

    # setupUi

    def retranslateUi(self, settings):
        settings.setWindowTitle(QCoreApplication.translate("settings", u"Dialog", None))
        self.view_rootfield_label.setText(QCoreApplication.translate("settings", u"Default view for Tree", None))
        self.view_rootfield.setItemText(0, QCoreApplication.translate("settings", u"Source", None))
        self.view_rootfield.setItemText(1, QCoreApplication.translate("settings", u"Tree", None))

        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_view), QCoreApplication.translate("settings", u"View", None))
        self.appearance_theme_label.setText(QCoreApplication.translate("settings", u"Theme", None))
        self.appearance_theme.setItemText(0, QCoreApplication.translate("settings", u"Default", None))

        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_appearance), QCoreApplication.translate("settings", u"Appearance", None))
        self.enableFindExperimentalLabel.setText(QCoreApplication.translate("settings", u"Enable find (experimental)", None))
        self.setting_tabs.setTabText(self.setting_tabs.indexOf(self.tab_debug), QCoreApplication.translate("settings", u"Debug", None))
    # retranslateUi

