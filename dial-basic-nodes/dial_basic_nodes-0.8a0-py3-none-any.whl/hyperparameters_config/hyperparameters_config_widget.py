# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from enum import Enum
from typing import Dict, Any, List


class HyperparametersConfigWidget:
    class Parameters(Enum):
        Epochs = "epochs"
        LossFunction = "loss_function"
        Optimizer = "optimizer"
        BatchSize = "batch_size"

    def __init__(self):

        self._available_optimizers = [
            "SGD",
            "RMSprop",
            "Adagrad",
            "Adadelta",
            "Adam",
            "Adamax",
            "Nadam",
        ]

        self._available_loss_functions = [
            "mean_squared_error",
            "mean_absolute_error",
            "mean_absolute_percentage_error",
            "mean_square_logarithmic_error",
            "squared_hinge",
            "hinge",
            "categorical_hinge",
            "logcosh",
            "huber_loss",
            "categorical_crossentropy",
            "sparse_categorical_crossentropy",
            "binary_crossentropy",
            "kullback_leibler_divergence",
            "poisson",
            "cosine_proximity",
            "is_categorical_crossentropy",
        ]

        self._hyperparameters = {
            self.Parameters.Epochs.value: 1,
            self.Parameters.LossFunction.value: self._available_loss_functions[0],
            self.Parameters.Optimizer.value: self._available_optimizers[0],
            self.Parameters.BatchSize.value: 32,
        }

    def get_hyperparameters(self):
        return self._hyperparameters

    def set_hyperparameters(self, hyperparameters: Dict[str, Any]):
        self.set_epochs(hyperparameters[self.Parameters.Epochs.value])
        self.set_loss_function(hyperparameters[self.Parameters.LossFunction.value])
        self.set_optimizer(hyperparameters[self.Parameters.Optimizer.value])
        self.set_batch_size(hyperparameters[self.Parameters.batch_size.value])

    def get_epochs(self) -> int:
        return self._hyperparameters[self.Parameters.Epochs.value]

    def set_epochs(self, epochs: int):
        self._hyperparameters[self.Parameters.Epochs.value] = epochs

    def get_loss_function(self) -> str:
        return self._hyperparameters[self.Parameters.LossFunction.value]

    def set_loss_function(self, loss_function: str):
        if loss_function not in self._available_loss_functions:
            raise ValueError(f"`{loss_function}` is an invalid loss function!")

        self._hyperparameters[self.Parameters.LossFunction.value] = loss_function

    def get_available_loss_functions(self) -> List[str]:
        return self._available_loss_functions

    def get_optimizer(self) -> str:
        return self._hyperparameters[self.Parameters.Optimizer.value]

    def set_optimizer(self, optimizer: str):
        if optimizer not in self._available_optimizers:
            raise ValueError(f"`{optimizer}` is an invalid optimizer!")

        self._hyperparameters[self.Parameters.Optimizer.value] = optimizer

    def get_available_optimizers(self) -> List[str]:
        return self._available_optimizers

    def get_batch_size(self) -> int:
        return self._hyperparameters[self.Parameters.BatchSize.value]

    def set_batch_size(self, batch_size: int):
        self._hyperparameters[self.Parameters.BatchSize.value] = batch_size


HyperparametersConfigWidgetFactory = providers.Factory(HyperparametersConfigWidget)
