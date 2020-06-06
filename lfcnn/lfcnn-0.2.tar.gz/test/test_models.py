# Copyright (C) 2020  The LFCNN Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Test lfcnn.models
"""
# Set CPU as device:
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import numpy as np

from tensorflow.keras.backend import clear_session
from tensorflow.keras import optimizers, Model, Input
from tensorflow.keras.layers import Activation

from lfcnn.losses import MeanSquaredError
from lfcnn.metrics import MeanSquaredError as MSE_metric
from lfcnn.metrics import MeanAbsoluteError as MAE_metric
from lfcnn.metrics import get_lf_metrics, PSNR
from lfcnn.models import BaseModel

from lfcnn.generators import LfGenerator
from lfcnn.generators.reshapes import lf_identity


class MockModel(BaseModel):

    def __init__(self, **kwargs):
        super(MockModel, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = LfGenerator
        self._reshape_func = lf_identity
        return

    def create_model(self, inputs, augmented_shape=None):
        out = Activation('relu', name='light_field')(inputs)
        return Model(inputs, out, name="MockModel")


def get_model_kwargs():
    optimizer = optimizers.SGD(learning_rate=0.1)
    loss = dict(light_field=MeanSquaredError())
    metrics = dict(light_field=get_lf_metrics())

    model_kwargs = dict(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics,
        callbacks=[]
    )

    return model_kwargs


def get_train_kwargs(generated_shape):
    dat = np.random.rand(8, 9, 9, 32, 32, 3)
    data = dict(data=dat)
    dat = np.random.rand(8, 9, 9, 32, 32, 3)
    valid_data = dict(data=dat)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=(9, 9, 32, 32, 3),
                        generated_shape=generated_shape,
                        batch_size=2,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def test_init():

    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    assert type(model.optimizer) == optimizers.SGD
    assert type(model.loss['light_field']) == MeanSquaredError
    assert type(model.metrics['light_field'][0]) == MAE_metric
    assert type(model.metrics['light_field'][1]) == MSE_metric
    assert type(model.metrics['light_field'][2]) == PSNR
    assert model.callbacks == []
    assert model.generator == LfGenerator
    assert model.reshape_func == lf_identity
    assert model.model_crop is None

    clear_session()
    return


def test_model_creation():

    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    assert model.keras_model is None

    generated_shape = [(9, 9, 32, 32, 3)]
    inputs = [Input(shape) for shape in generated_shape]
    model.__create_model__(inputs, (9, 9, 32, 32, 3), gpus=1, cpu_merge=False)
    assert type(model.keras_model) == Model
    assert model.keras_model.name == "MockModel"

    # Model is compiled and should be trainable
    model.keras_model.fit(np.random.rand(8, 9, 9, 32, 32, 3))
    
    clear_session()
    return
