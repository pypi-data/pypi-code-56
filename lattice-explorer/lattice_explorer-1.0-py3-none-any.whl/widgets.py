# Lattice Explorer
# Copyright (C) 2020  Dominik Vilsmeier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from collections.abc import Sequence

from arguable import Arguable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSlider


class ConfigWidget(Arguable, QWidget):
    """Widget that can be configured via Namespace objects and command line arguments."""

    config_removesuffix = 'widget'


class LabeledHSlider(QWidget):
    """Slider with tick labels."""

    def __init__(self, a, b):
        super().__init__()
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(a, b)
        self._slider.setTickInterval(1)
        self._slider.setTickPosition(QSlider.TicksAbove)

        labels_layout = QHBoxLayout()
        for tick in range(a, b+1):
            label = QLabel(str(tick))
            label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            labels_layout.addWidget(label)

        layout = QVBoxLayout()
        layout.addLayout(labels_layout)
        layout.addWidget(self._slider)
        self.setLayout(layout)

    def __getattr__(self, name):
        return getattr(self._slider, name)
