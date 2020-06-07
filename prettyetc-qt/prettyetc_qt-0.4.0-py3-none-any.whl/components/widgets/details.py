# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'details.ui'
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


class Ui_FieldDetails(object):
    def setupUi(self, FieldDetails):
        if not FieldDetails.objectName():
            FieldDetails.setObjectName(u"FieldDetails")
        FieldDetails.resize(400, 583)
        self.verticalLayout = QVBoxLayout(FieldDetails)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(FieldDetails)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.title.setFont(font)
        self.title.setScaledContents(True)
        self.title.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.title.setWordWrap(True)

        self.verticalLayout.addWidget(self.title)

        self.details_container = QWidget(FieldDetails)
        self.details_container.setObjectName(u"details_container")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.details_container.sizePolicy().hasHeightForWidth())
        self.details_container.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.details_container)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setContentsMargins(10, 20, 10, 1)
        self.nameLabel = QLabel(self.details_container)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nameLabel)

        self.fieldname = QLineEdit(self.details_container)
        self.fieldname.setObjectName(u"fieldname")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.fieldname)

        self.dataLabel = QLabel(self.details_container)
        self.dataLabel.setObjectName(u"dataLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.dataLabel)

        self.fielddata = QLineEdit(self.details_container)
        self.fielddata.setObjectName(u"fielddata")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fielddata)

        self.descriptionLabel = QLabel(self.details_container)
        self.descriptionLabel.setObjectName(u"descriptionLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.descriptionLabel)

        self.field_description = QPlainTextEdit(self.details_container)
        self.field_description.setObjectName(u"field_description")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.field_description.sizePolicy().hasHeightForWidth())
        self.field_description.setSizePolicy(sizePolicy1)
        self.field_description.setMinimumSize(QSize(0, 29))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.field_description)

        self.readonlyLabel = QLabel(self.details_container)
        self.readonlyLabel.setObjectName(u"readonlyLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.readonlyLabel)

        self.field_readonly = QCheckBox(self.details_container)
        self.field_readonly.setObjectName(u"field_readonly")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.field_readonly)

        self.line = QFrame(self.details_container)
        self.line.setObjectName(u"line")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy2)
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QFrame.HLine)

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.line)

        self.details_label = QLabel(self.details_container)
        self.details_label.setObjectName(u"details_label")
        font1 = QFont()
        font1.setBold(True)
        font1.setWeight(75)
        self.details_label.setFont(font1)
        self.details_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.formLayout.setWidget(6, QFormLayout.SpanningRole, self.details_label)

        self.field_attributes = QTreeWidget(self.details_container)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.field_attributes.setHeaderItem(__qtreewidgetitem)
        self.field_attributes.setObjectName(u"field_attributes")
        sizePolicy1.setHeightForWidth(self.field_attributes.sizePolicy().hasHeightForWidth())
        self.field_attributes.setSizePolicy(sizePolicy1)
        self.field_attributes.header().setMinimumSectionSize(42)
        self.field_attributes.header().setHighlightSections(True)

        self.formLayout.setWidget(7, QFormLayout.SpanningRole, self.field_attributes)


        self.verticalLayout.addWidget(self.details_container)

#if QT_CONFIG(shortcut)
        self.nameLabel.setBuddy(self.fieldname)
        self.dataLabel.setBuddy(self.fielddata)
        self.readonlyLabel.setBuddy(self.field_readonly)
        self.details_label.setBuddy(self.field_attributes)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(FieldDetails)
    # setupUi

    def retranslateUi(self, FieldDetails):
        FieldDetails.setWindowTitle(QCoreApplication.translate("FieldDetails", u"Frame", None))
        self.title.setText(QCoreApplication.translate("FieldDetails", u"<html><head/><body><p><span style=\" font-size:22pt;\">Field properties</span></p></body></html>", None))
        self.nameLabel.setText(QCoreApplication.translate("FieldDetails", u"Name", None))
        self.dataLabel.setText(QCoreApplication.translate("FieldDetails", u"Data", None))
        self.descriptionLabel.setText(QCoreApplication.translate("FieldDetails", u"Description", None))
        self.readonlyLabel.setText(QCoreApplication.translate("FieldDetails", u"Readonly", None))
        self.field_readonly.setText("")
        self.details_label.setText(QCoreApplication.translate("FieldDetails", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:400;\">Attributes</span></p></body></html>", None))
        ___qtreewidgetitem = self.field_attributes.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("FieldDetails", u"value", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("FieldDetails", u"name", None));
    # retranslateUi

