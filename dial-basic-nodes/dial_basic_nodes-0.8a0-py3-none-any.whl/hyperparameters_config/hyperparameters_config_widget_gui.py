# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

import dependency_injector.providers as providers
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QComboBox, QFormLayout, QSpinBox, QWidget

from .hyperparameters_config_widget import HyperparametersConfigWidget


class HyperparametersConfigWidgetGui(QWidget, HyperparametersConfigWidget):
    def __init__(self, parent: "QWidget" = None):
        HyperparametersConfigWidget.__init__(self)
        QWidget.__init__(self, parent)

        # Widgets
        self._epoch_spinbox = QSpinBox(parent=self)
        self._epoch_spinbox.setMinimum(1)
        self._epoch_spinbox.setValue(self.get_epochs())

        self._loss_function_combobox = QComboBox(parent=self)
        self._loss_function_combobox.addItems(self.get_available_loss_functions())
        self._loss_function_combobox.setCurrentText(self.get_loss_function())

        self._optimizer_combobox = QComboBox()
        self._optimizer_combobox.addItems(self.get_available_optimizers())
        self._optimizer_combobox.setCurrentText(self.get_optimizer())

        self._batch_size_spinbox = QSpinBox(parent=self)
        self._batch_size_spinbox.setValue(self.get_batch_size())
        self._batch_size_spinbox.setMinimum(1)
        self._batch_size_spinbox.setMaximum(999999)

        # Layouts
        self._main_layout = QFormLayout()
        self._main_layout.addRow("Epochs", self._epoch_spinbox)
        self._main_layout.addRow("Optimizer", self._optimizer_combobox)
        self._main_layout.addRow("Loss function", self._loss_function_combobox)
        self._main_layout.addRow("Batch size", self._batch_size_spinbox)
        self.setLayout(self._main_layout)

        # Hyperparameters dictionary
        self._epoch_spinbox.valueChanged.connect(self.set_epochs)
        self._loss_function_combobox.currentTextChanged.connect(self.set_loss_function)
        self._optimizer_combobox.currentTextChanged.connect(self.set_optimizer)
        self._batch_size_spinbox.valueChanged.connect(self.set_batch_size)

    def set_epochs(self, epochs: int):
        super().set_epochs(epochs)

        self._epoch_spinbox.setValue(epochs)

    def set_loss_function(self, loss_function: str):
        super().set_loss_function(loss_function)

        self._loss_function_combobox.setCurrentText(loss_function)

    def set_optimizer(self, optimizer: str):
        super().set_optimizer(optimizer)

        self._optimizer_combobox.setCurrentText(optimizer)

    def set_batch_size(self, batch_size: int):
        super().set_batch_size(batch_size)

        self._batch_size_spinbox.setValue(batch_size)

    def sizeHint(self) -> "QSize":
        return QSize(350, 200)

    def __getstate__(self):
        return {"hyperparameters": self.get_hyperparameters()}

    def __setstate__(self, new_state):
        self._hyperparameters = new_state["hyperparameters"]

        self.set_hyperparameters(new_state["hyperparameters"])

    def __reduce__(self):
        return (HyperparametersConfigWidgetGui, (), self.__getstate__())


HyperparametersConfigWidgetGuiFactory = providers.Factory(
    HyperparametersConfigWidgetGui
)
