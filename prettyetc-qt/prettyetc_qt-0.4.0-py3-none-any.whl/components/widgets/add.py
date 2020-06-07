# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add.ui'
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


class Ui_add_dialog(object):
    def setupUi(self, add_dialog):
        if not add_dialog.objectName():
            add_dialog.setObjectName(u"add_dialog")
        add_dialog.resize(454, 377)
        self.root_layout = QVBoxLayout(add_dialog)
        self.root_layout.setObjectName(u"root_layout")
        self.label = QLabel(add_dialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.root_layout.addWidget(self.label)

        self.details_container = QWidget(add_dialog)
        self.details_container.setObjectName(u"details_container")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.details_container.sizePolicy().hasHeightForWidth())
        self.details_container.setSizePolicy(sizePolicy)
        self.formLayout_2 = QFormLayout(self.details_container)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(20)
        self.formLayout_2.setVerticalSpacing(20)
        self.formLayout_2.setContentsMargins(10, 20, 10, 1)
        self.nameLabel = QLabel(self.details_container)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.nameLabel)

        self.fieldname = QLineEdit(self.details_container)
        self.fieldname.setObjectName(u"fieldname")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.fieldname)

        self.dataLabel = QLabel(self.details_container)
        self.dataLabel.setObjectName(u"dataLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.dataLabel)

        self.fielddata = QLineEdit(self.details_container)
        self.fielddata.setObjectName(u"fielddata")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.fielddata)

        self.descriptionLabel = QLabel(self.details_container)
        self.descriptionLabel.setObjectName(u"descriptionLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.descriptionLabel)

        self.field_description = QLineEdit(self.details_container)
        self.field_description.setObjectName(u"field_description")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.field_description)

        self.readonlyLabel = QLabel(self.details_container)
        self.readonlyLabel.setObjectName(u"readonlyLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.readonlyLabel)

        self.field_readonly = QCheckBox(self.details_container)
        self.field_readonly.setObjectName(u"field_readonly")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.field_readonly)

        self.typeLabel = QLabel(self.details_container)
        self.typeLabel.setObjectName(u"typeLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.typeLabel)

        self.field_type = QComboBox(self.details_container)
        self.field_type.addItem("")
        self.field_type.addItem("")
        self.field_type.addItem("")
        self.field_type.addItem("")
        self.field_type.addItem("")
        self.field_type.addItem("")
        self.field_type.setObjectName(u"field_type")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.field_type)

        self.buttonbox = QDialogButtonBox(self.details_container)
        self.buttonbox.setObjectName(u"buttonbox")
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.buttonbox)


        self.root_layout.addWidget(self.details_container)

#if QT_CONFIG(shortcut)
        self.nameLabel.setBuddy(self.fieldname)
        self.dataLabel.setBuddy(self.fielddata)
        self.descriptionLabel.setBuddy(self.field_description)
        self.readonlyLabel.setBuddy(self.field_readonly)
        self.typeLabel.setBuddy(self.field_type)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(add_dialog)
        self.buttonbox.accepted.connect(add_dialog.accept)
        self.buttonbox.rejected.connect(add_dialog.reject)
    # setupUi

    def retranslateUi(self, add_dialog):
        add_dialog.setWindowTitle(QCoreApplication.translate("add_dialog", u"Add field", None))
        self.label.setText(QCoreApplication.translate("add_dialog", u"<html><head/><body><p><span style=\" font-size:24pt;\">Add new field</span></p></body></html>", None))
        self.nameLabel.setText(QCoreApplication.translate("add_dialog", u"Name", None))
        self.dataLabel.setText(QCoreApplication.translate("add_dialog", u"Data", None))
        self.descriptionLabel.setText(QCoreApplication.translate("add_dialog", u"Description", None))
        self.readonlyLabel.setText(QCoreApplication.translate("add_dialog", u"Readonly", None))
        self.field_readonly.setText("")
        self.typeLabel.setText(QCoreApplication.translate("add_dialog", u"Type", None))
        self.field_type.setItemText(0, QCoreApplication.translate("add_dialog", u"Text", None))
        self.field_type.setItemText(1, QCoreApplication.translate("add_dialog", u"Integer number", None))
        self.field_type.setItemText(2, QCoreApplication.translate("add_dialog", u"Decimal number", None))
        self.field_type.setItemText(3, QCoreApplication.translate("add_dialog", u"True/False (boolean)", None))
        self.field_type.setItemText(4, QCoreApplication.translate("add_dialog", u"Collection of ordered fields", None))
        self.field_type.setItemText(5, QCoreApplication.translate("add_dialog", u"Collection of unique fields", None))

    # retranslateUi

