# Video Browser
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


from argparse import Namespace
from contextlib import contextmanager
from functools import partial
import logging
from pathlib import Path
from pprint import pformat
import sys

from arguable import Arguable
import cv2 as cv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,
    QLineEdit, QMessageBox, QShortcut, QSpinBox, QComboBox, QLabel
)


logger = logging.getLogger(__name__)


@contextmanager
def temporary_deactivate(*widgets):
    for widget in widgets:
        widget.setEnabled(False)
    yield
    for widget in widgets:
        widget.setEnabled(True)


@contextmanager
def temporary_disconnect(signal, slot):
    try:
        signal.disconnect(slot)
    except TypeError:
        was_connected = False
    else:
        was_connected = True
    yield
    if was_connected:
        signal.connect(slot)


class ConfigWidget(Arguable, QWidget):
    """Subclasses of this type are configurable via Namespace 'config' objects."""

    config_removesuffix = 'widget'


class VideoBrowser(QMainWindow):
    """Main window hosting all other widgets."""

    def __init__(self, video_dir):
        super().__init__()
        self.setWindowTitle('Video Browser')
        self.ui = UIWidget(video_dir)
        self.setCentralWidget(self.ui)


class UIWidget(ConfigWidget):
    """Main widget hosting the controls and the frames canvas."""

    config = Namespace(
        cache_limit_in_pixels = 500_000_000,
        default_file_suffix = 'ts',
    )

    def __init__(self, video_dir):
        super().__init__()
        self.controls = {
            'video_filter': QLineEdit(),
            'video_list': QComboBox(),
            'prev_frame': QPushButton('<'),
            'frame_counter': QSpinBox(),
            'frame_number': QLabel(),
            'next_frame': QPushButton('>'),
            'apply_median_filter_3': QPushButton('Median Filter (3)'),
            'apply_median_filter_5': QPushButton('Median Filter (5)'),
            'apply_denoising': QPushButton('Denoising'),
            'apply_grayscale': QPushButton('Grayscale'),
            'roi': QPushButton('ROI'),
        }
        self.controls['video_filter'].setPlaceholderText('globbing filter')
        controls_layout = QHBoxLayout()
        for widget in self.controls.values():
            controls_layout.addWidget(widget)
        controls_layout.addStretch(1)
        self.canvas = Canvas()
        self.toolbar = NavigationToolbar2QT(self.canvas, parent=self)
        layout = QVBoxLayout()
        layout.addLayout(controls_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.video_cache = {
            'frames': {},
            'names': [],
            'count': 0,
            'limit': self.config.cache_limit_in_pixels,
        }

        self.video_dir = Path(video_dir)
        self.video_list = []

        self.frames = []
        self.frame_counter = 0

        self.update_video_list()

        self.controls['video_filter'].editingFinished.connect(self.update_video_list)
        self.controls['video_list'].currentIndexChanged.connect(self.next_video)
        self.controls['prev_frame'].clicked.connect(self.prev_frame)
        self.controls['next_frame'].clicked.connect(self.next_frame)
        self.controls['frame_counter'].valueChanged.connect(self.frame_counter_changed)
        self.controls['apply_median_filter_3'].clicked.connect(
            partial(self.canvas.apply_median_filter, kernel_size=3))
        self.controls['apply_median_filter_5'].clicked.connect(
            partial(self.canvas.apply_median_filter, kernel_size=5))
        self.controls['apply_denoising'].clicked.connect(self.canvas.apply_denoising)
        self.controls['apply_grayscale'].clicked.connect(self.canvas.apply_grayscale)
        self.controls['roi'].clicked.connect(self.submit_region_of_interest)

        self.controls['prev_frame'].setShortcut(QKeySequence(Qt.Key_Left))
        self.controls['next_frame'].setShortcut(QKeySequence(Qt.Key_Right))

    def update_video_list(self):
        """Update the video list based on the video filter or using the default file suffix."""
        with temporary_deactivate(*self.controls.values()):
            pattern = str(self.controls['video_filter'].text()) or f'*.{self.config.default_file_suffix}'
            logger.info(f'Update video list with pattern {pattern!r}')
            new_video_list = sorted(self.video_dir.glob(pattern))
            if new_video_list == self.video_list:
                logger.info('Update video list: nothing changed')
                return
            with temporary_disconnect(self.controls['video_list'].currentIndexChanged, self.next_video):
                while self.controls['video_list'].count() > 0:
                    self.controls['video_list'].removeItem(0)
                self.video_list = new_video_list
                for path in self.video_list:
                    self.controls['video_list'].addItem(path.stem, path)
            self.next_video(self.controls['video_list'].currentIndex())

    def submit_region_of_interest(self):
        """Print the current axes limits of the frame canvas to stdout and show a corresponding dialog."""
        roi = self.canvas.get_region_of_interest()
        print(f'ROI: {roi!r}')
        InfoBox('Region Of Interest', pformat(roi))

    def next_video(self, index):
        """Load the video located at the given index."""
        with temporary_deactivate(*self.controls.values()):
            try:
                path = str(self.video_list[index])
            except IndexError:
                return
            if path in self.video_cache['frames']:
                self.frames = self.video_cache['frames'][path]
                self.video_cache['names'].remove(path)
                self.video_cache['names'].append(path)  # Move `path` to the end of the list.
            else:
                video = cv.VideoCapture(path)
                frames = []
                while video.isOpened():
                    ret, frame = video.read()
                    if not ret:
                        break
                    frames.append(frame)
                video.release()
                self.frames = np.stack(frames)

                while self.video_cache['count'] + self.frames.size > self.video_cache['limit']:
                    dropped = self.video_cache['frames'].pop(self.video_cache['names'].pop(0))
                    self.video_cache['count'] -= dropped.size
                    del dropped

                self.video_cache['frames'][path] = self.frames
                self.video_cache['names'].append(path)

            self.frame_counter = min(self.frame_counter, len(self.frames) - 1)
            self.controls['frame_counter'].setRange(1, len(self.frames))
            self.controls['frame_number'].setText(f'({len(self.frames)})')
            logger.info('Video loaded: %s', path)
            self.load_frame()

    def frame_counter_changed(self, value):
        self.frame_counter = value - 1  # The UI is 1-based.
        self.load_frame()

    def next_frame(self):
        self.frame_counter += 1
        self.new_frame()

    def prev_frame(self):
        self.frame_counter -= 1
        self.new_frame()

    def new_frame(self):
        self.frame_counter %= len(self.frames)
        self.controls['frame_counter'].setValue(self.frame_counter + 1)

    def load_frame(self):
        self.canvas.new_frame(self.frames[self.frame_counter])


class Canvas(ConfigWidget, FigureCanvasQTAgg):
    """Canvas displaying the video frames."""

    config = Namespace(
        figsize_inches = (9.6, 8.4),
    )

    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.fig.set_size_inches(self.config.figsize_inches)
        self.ax = self.fig.add_subplot(111)
        self.frame = None

    def get_region_of_interest(self):
        return dict(x=self.ax.get_xlim(), y=self.ax.get_ylim())

    def apply_grayscale(self):
        if len(self.frame.shape) > 2:
            self.new_frame(cv.cvtColor(self.frame, cv.COLOR_RGB2GRAY))
        else:
            logger.info('The current frame uses already grayscale')

    def apply_median_filter(self, *, kernel_size):
        self.new_frame(cv.medianBlur(self.frame, kernel_size))

    def apply_denoising(self):
        self.new_frame(cv.fastNlMeansDenoising(self.frame))

    def new_frame(self, frame):
        self.ax.cla()
        self.ax.imshow(frame)
        self.draw()
        self.frame = frame


class InfoBox(QMessageBox):
    def __init__(self, title, msg):
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)
        self.setText(msg)
        self.exec_()
