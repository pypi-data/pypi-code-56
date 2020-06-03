# vim: set fileencoding=utf-8 :
###############################################################################
#                                                                             #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.editor module of the BEAT platform.           #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################

import random

import pytest

from PyQt5 import QtCore
from PyQt5.QtWidgets import QInputDialog

from ..backend.assetmodel import DataFormatModel
from ..widgets.dataformateditor import DataformatArrayWidget
from ..widgets.dataformateditor import DataformatEditor
from ..widgets.dataformateditor import DataformatObjectWidget
from ..widgets.dataformateditor import DataformatWidget
from ..widgets.dataformateditor import default_dataformat
from ..widgets.dataformateditor import default_object_dataformat


@pytest.fixture()
def dataformat_model(test_prefix):
    asset_model = DataFormatModel()
    asset_model.full_list_enabled = True
    asset_model.prefix_path = test_prefix
    return asset_model


def get_random_dataformat(dataformat_model):
    index = random.randint(0, dataformat_model.rowCount() - 1)
    model_index = dataformat_model.index(index, 0)
    return model_index.data()


class TestDataformatWidget:
    """Test that the mock editor works correctly"""

    def test_load_and_dump(self, qtbot, dataformat_model):
        name = "test"
        value = get_random_dataformat(dataformat_model)
        reference_json = {name: value}

        editor = DataformatWidget(dataformat_model)
        qtbot.addWidget(editor)

        editor.load(None, value)

        assert editor.dump() == value

        editor.load(name, value)

        assert editor.dump() == reference_json


class TestDataformatObjectWidget:
    """Test that the mock editor works correctly"""

    def test_load_and_dump(self, qtbot, dataformat_model):
        name = "test"
        dataformat = get_random_dataformat(dataformat_model)

        value = {"key": dataformat}
        reference_json = {name: value}

        editor = DataformatObjectWidget(dataformat_model)
        qtbot.addWidget(editor)

        editor.load(None, value)

        assert editor.dump() == value

        editor.load(name, value)

        assert editor.dump() == reference_json

    def test_add(self, qtbot, monkeypatch, dataformat_model):
        editor = DataformatObjectWidget(dataformat_model)
        qtbot.addWidget(editor)

        model_index = dataformat_model.index(0, 0)
        value = model_index.data()
        reference_json = {"test_type": value}

        monkeypatch.setattr(
            QInputDialog, "getText", classmethod(lambda *args: ("test_type", True))
        )
        editor.add_type_action.trigger()

        assert editor.dump() == reference_json

        monkeypatch.setattr(
            QInputDialog, "getText", classmethod(lambda *args: ("test_object", True))
        )
        editor.add_object_action.trigger()
        reference_json["test_object"] = default_object_dataformat()

        assert editor.dump() == reference_json

        monkeypatch.setattr(
            QInputDialog,
            "getText",
            classmethod(lambda *args: ("test_type_array", True)),
        )
        editor.add_type_array_action.trigger()
        reference_json["test_type_array"] = [0, DEFAULT_TYPE]

        assert editor.dump() == reference_json

        monkeypatch.setattr(
            QInputDialog,
            "getText",
            classmethod(lambda *args: ("test_object_array", True)),
        )
        editor.add_object_array_action.trigger()
        reference_json["test_object_array"] = [0, default_object_dataformat()]

        assert editor.dump() == reference_json


class TestDataformatArrayWidget:
    """Test that the mock editor works correctly"""

    def test_load_and_dump(self, qtbot, dataformat_model):
        name = "test"
        dataformat = get_random_dataformat(dataformat_model)

        value = [0, {"key": dataformat}]
        reference_json = {name: value}

        editor = DataformatArrayWidget(dataformat_model)
        qtbot.addWidget(editor)

        editor.load(None, value)

        assert editor.dump() == value

        editor.load(name, value)

        assert editor.dump() == reference_json

    def test_dimension(self, qtbot, dataformat_model):
        model_index = dataformat_model.index(0, 0)
        dataformat = model_index.data()
        value = [0, dataformat]

        editor = DataformatArrayWidget(dataformat_model)
        qtbot.addWidget(editor)

        editor.load(None, value)

        assert editor.dump() == value

        qtbot.mouseClick(editor.add_dimension_button, QtCore.Qt.LeftButton)

        assert editor.dump() == [0, 0, dataformat]

        with qtbot.waitSignal(editor.dataChanged):
            editor.dimension_widgets[0].setValue(12)

        with qtbot.waitSignal(editor.dataChanged):
            editor.dimension_widgets[1].setValue(13)

        assert editor.dump() == [12, 13, dataformat]


DEFAULT_TYPE = default_dataformat()


class TestDataformatEditor:
    """Test that the mock editor works correctly"""

    @pytest.mark.parametrize(
        "reference_json",
        [
            {"#description": "test"},
            {"#extends": "test/test/1"},
            {"#schema_version": 1},
            {"#description": "test", "#extends": "test/test/1"},
            {"#description": "test", "#schema_version": 1},
            {"#extends": "test/test/1", "#schema_version": 1},
            {"#description": "test", "#extends": "test/test/1", "#schema_version": 1},
        ],
    )
    def test_load_and_dump_meta_data(self, qtbot, reference_json):
        editor = DataformatEditor()
        qtbot.addWidget(editor)

        editor.load_json(reference_json)

        assert editor.dump_json() == reference_json
        validated, errors = editor.is_valid()
        assert validated, errors

    @pytest.mark.parametrize(
        "reference_json",
        [
            {"type": DEFAULT_TYPE},
            {"object": {"test1": DEFAULT_TYPE}},
            {"list": [0, DEFAULT_TYPE]},
            {"array": [0, 0, DEFAULT_TYPE]},
            {"list_of_object": [0, {"test1": DEFAULT_TYPE}]},
            {"array_of_object": [0, 0, {"test1": DEFAULT_TYPE}]},
        ],
    )
    def test_load_and_dump_data(self, qtbot, monkeypatch, beat_context, reference_json):
        editor = DataformatEditor()
        qtbot.addWidget(editor)
        editor.set_context(beat_context)

        editor.load_json(reference_json)

        assert editor.dump_json() == reference_json
        validated, errors = editor.is_valid()
        assert validated, errors

    def test_add(self, qtbot, monkeypatch, beat_context, dataformat_model):
        editor = DataformatEditor()
        qtbot.addWidget(editor)
        editor.set_context(beat_context)

        model_index = dataformat_model.index(0, 0)
        value = model_index.data()

        monkeypatch.setattr(
            QInputDialog, "getText", classmethod(lambda *args: ("test_type", True))
        )
        editor.add_type_action.trigger()
        reference_json = {"test_type": value}

        assert editor.dump_json() == reference_json
        validated, errors = editor.is_valid()
        assert validated, errors

        monkeypatch.setattr(
            QInputDialog, "getText", classmethod(lambda *args: ("test_object", True))
        )
        editor.add_object_action.trigger()
        reference_json["test_object"] = default_object_dataformat()

        assert editor.dump_json() == reference_json
        validated, errors = editor.is_valid()
        assert validated, errors

        monkeypatch.setattr(
            QInputDialog,
            "getText",
            classmethod(lambda *args: ("test_type_array", True)),
        )
        editor.add_type_array_action.trigger()
        reference_json["test_type_array"] = [0, DEFAULT_TYPE]

        assert editor.dump_json() == reference_json
        validated, errors = editor.is_valid()
        assert validated, errors

        monkeypatch.setattr(
            QInputDialog,
            "getText",
            classmethod(lambda *args: ("test_object_array", True)),
        )
        editor.add_object_array_action.trigger()
        reference_json["test_object_array"] = [0, default_object_dataformat()]

        assert editor.dump_json() == reference_json
        validated, errors = editor.is_valid()
        assert validated, errors
