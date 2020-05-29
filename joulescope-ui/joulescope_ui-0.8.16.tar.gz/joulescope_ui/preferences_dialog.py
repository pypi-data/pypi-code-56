# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        if not PreferencesDialog.objectName():
            PreferencesDialog.setObjectName(u"PreferencesDialog")
        PreferencesDialog.resize(660, 388)
        PreferencesDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(PreferencesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.profileWidget = QWidget(PreferencesDialog)
        self.profileWidget.setObjectName(u"profileWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.profileWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.profileLabel = QLabel(self.profileWidget)
        self.profileLabel.setObjectName(u"profileLabel")

        self.horizontalLayout_3.addWidget(self.profileLabel)

        self.profileComboBox = QComboBox(self.profileWidget)
        self.profileComboBox.setObjectName(u"profileComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileComboBox.sizePolicy().hasHeightForWidth())
        self.profileComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.profileComboBox)

        self.profileActivateButton = QPushButton(self.profileWidget)
        self.profileActivateButton.setObjectName(u"profileActivateButton")

        self.horizontalLayout_3.addWidget(self.profileActivateButton)

        self.profileResetButton = QPushButton(self.profileWidget)
        self.profileResetButton.setObjectName(u"profileResetButton")

        self.horizontalLayout_3.addWidget(self.profileResetButton)

        self.profileNewButton = QPushButton(self.profileWidget)
        self.profileNewButton.setObjectName(u"profileNewButton")

        self.horizontalLayout_3.addWidget(self.profileNewButton)

        self.profileHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.profileHorizontalSpacer)

        self.helpButton = QPushButton(self.profileWidget)
        self.helpButton.setObjectName(u"helpButton")

        self.horizontalLayout_3.addWidget(self.helpButton)


        self.verticalLayout.addWidget(self.profileWidget)

        self.widget = QWidget(PreferencesDialog)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.treeView = QTreeView(self.widget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setAnimated(True)
        self.treeView.header().setVisible(False)

        self.horizontalLayout.addWidget(self.treeView)

        self.scrollArea = QScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.targetWidget = QWidget()
        self.targetWidget.setObjectName(u"targetWidget")
        self.targetWidget.setGeometry(QRect(0, 0, 307, 254))
        self.formLayout_2 = QFormLayout(self.targetWidget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.scrollArea.setWidget(self.targetWidget)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.verticalLayout.addWidget(self.widget)

        self.buttonFrame = QFrame(PreferencesDialog)
        self.buttonFrame.setObjectName(u"buttonFrame")
        self.buttonFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.buttonFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.resetButton = QPushButton(self.buttonFrame)
        self.resetButton.setObjectName(u"resetButton")

        self.horizontalLayout_2.addWidget(self.resetButton)

        self.cancelButton = QPushButton(self.buttonFrame)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.okButton = QPushButton(self.buttonFrame)
        self.okButton.setObjectName(u"okButton")

        self.horizontalLayout_2.addWidget(self.okButton)


        self.verticalLayout.addWidget(self.buttonFrame)


        self.retranslateUi(PreferencesDialog)

        QMetaObject.connectSlotsByName(PreferencesDialog)
    # setupUi

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QCoreApplication.translate("PreferencesDialog", u"Preferences", None))
        self.profileLabel.setText(QCoreApplication.translate("PreferencesDialog", u"Profile", None))
#if QT_CONFIG(tooltip)
        self.profileComboBox.setToolTip(QCoreApplication.translate("PreferencesDialog", u"Select the profile to view and edit.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.profileActivateButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Activate the selected profile.</span></p><p>This action updates Joulescope UI to use the preferences in the selected profile.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.profileActivateButton.setText(QCoreApplication.translate("PreferencesDialog", u"Activate", None))
#if QT_CONFIG(tooltip)
        self.profileResetButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Reset or erase the selected profile.</span></p><p>For the built-in profiles, <span style=\" font-weight:600;\">Reset</span> the profile to the factory defaults.  For custom profiles, <span style=\" font-weight:600;\">Erase</span> the profile so that it is no longer available.  You cannot erase the built-in profiles.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.profileResetButton.setText(QCoreApplication.translate("PreferencesDialog", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.profileNewButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html><head/><body><p>Create a new custom profile.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.profileNewButton.setText(QCoreApplication.translate("PreferencesDialog", u"New", None))
        self.helpButton.setText(QCoreApplication.translate("PreferencesDialog", u"Help", None))
#if QT_CONFIG(tooltip)
        self.treeView.setToolTip(QCoreApplication.translate("PreferencesDialog", u"Select the Preferences Group to display.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.scrollArea.setToolTip(QCoreApplication.translate("PreferencesDialog", u"View and edit the Preferences for the selected Profile and Preference Group.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.resetButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Reset the Preferences for the selected Profile and Preferences Group.</span></p><p>This button only resets the Preferences that are currently shown in the right-hand side, and only for the selected Profile.  All other preference values are not changed.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.resetButton.setText(QCoreApplication.translate("PreferencesDialog", u"Reset to Defaults", None))
        self.cancelButton.setText(QCoreApplication.translate("PreferencesDialog", u"Cancel", None))
        self.okButton.setText(QCoreApplication.translate("PreferencesDialog", u"OK", None))
    # retranslateUi

