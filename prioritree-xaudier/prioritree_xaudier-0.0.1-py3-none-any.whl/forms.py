# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSizePolicy, QFormLayout, QApplication, QLineEdit, QLabel, QGridLayout, QFrame, QDialogButtonBox, QPushButton, QDialog, QSpinBox 

class NewGenericForm(QDialog):
    def __init__(self, *args, attribute_dict={}, **kwargs):
        super(NewGenericForm, self).__init__(*args, **kwargs)
        self.attribute_dict=attribute_dict
        self.setupUi()
        self.show()

    def setFormAtributes(self, attribute_dict={}):
        self.attribute_dict = attribute_dict
        self.cleanAttributeFormat()

    def cleanAttributeFormat(self):
        if not self.attribute_dict:
            return

    def setupUi(self):
        self.setObjectName("NewTaskForm")
        self.setEnabled(True)
        self.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        # Form
        self.formLayout = QFormLayout(self)
        self.formLayout.setObjectName("formLayout")

        self.form = QWidget(self)
        self.form.setLayout(self.formLayout)

        for attr_idx, (attr_key, attr_style) in enumerate(self.attribute_dict.items()):
            if attr_style is "text":
                attrLabel = QLabel(self)
                attrLabel.setObjectName(attr_key + "Label")
                attrLabel.setText(attr_key)
                self.formLayout.setWidget(attr_idx, QFormLayout.LabelRole, attrLabel)
                attrLineEdit = QLineEdit(self)
                attrLineEdit.setObjectName(attr_key + "LineEdit")
                self.formLayout.setWidget(attr_idx, QFormLayout.FieldRole, attrLineEdit)
            if attr_style is "int":
                attrLabel = QLabel(self)
                attrLabel.setObjectName(attr_key + "Label")
                attrLabel.setText(attr_key)
                self.formLayout.setWidget(attr_idx, QFormLayout.LabelRole, attrLabel)
                attrSpinBox = QSpinBox(self)
                attrSpinBox.setMinimum(0)
                attrSpinBox.setMaximum(100)
                attrSpinBox.setObjectName(attr_key + "SpinBox")
                self.formLayout.setWidget(attr_idx, QFormLayout.FieldRole, attrSpinBox)

        # Buttons
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.okButton.setDefault(True)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancelButton, QDialogButtonBox.RejectRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Grid
        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.form)
        self.gridLayout.addWidget(self.buttonBox)

        # self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def sendDataBack(self):
        ret_dict={}
        for attr_key, attr_style in self.attribute_dict.items():
            if attr_style is "text":
                ret_dict[attr_key] = str(self.findChild(QLineEdit, attr_key + "LineEdit").text())
            if attr_style is "int":
                ret_dict[attr_key] = str(self.findChild(QSpinBox, attr_key + "SpinBox").value())
        return ret_dict

    # def retranslateUi(self):
    #     _translate = QtCore.QCoreApplication.translate
    #     self.setWindowTitle(_translate("NewTaskForm", "Form"))
    #     self.label.setText(_translate("NewTaskForm", "Title"))
    #     self.label_2.setText(_translate("NewTaskForm", "Description"))
    #     self.label_3.setText(_translate("NewTaskForm", "Urgency"))

class NewTaskForm(NewGenericForm):
    def __init__(self, *args, **kwargs):
        super(NewTaskForm, self).__init__(*args, attribute_dict={"Title":"text", "Description":"text", "Urgency":"int", "Importance":"int", "Priority":"int"}, **kwargs)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    newTaskForm = NewTaskForm()
    newTaskForm.show()
    sys.exit(app.exec_())

