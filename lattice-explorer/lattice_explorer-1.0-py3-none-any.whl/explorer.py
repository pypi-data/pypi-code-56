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


from argparse import Namespace
from collections import defaultdict
from functools import partial
import itertools as it
import logging
import math
from pathlib import Path

from cpymad.madx import Madx, TwissFailed
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QCheckBox,
    QGroupBox, QDoubleSpinBox, QScrollArea,
)

from .parser import find_all_commands
from .widgets import ConfigWidget, LabeledHSlider


logger = logging.getLogger(__name__)


class LatticeExplorer(QMainWindow):
    """Main window serving as an entry point to the application."""

    def __init__(self, f_path: str):
        super().__init__()
        self.setWindowTitle('Lattice Explorer')
        self.main = MainWidget(f_path)
        self.setCentralWidget(self.main)

    def closeEvent(self, event):
        self.main.controls_widget.close()
        event.accept()


class MainWidget(QWidget):
    """Main widget hosting the GUI and spawning the Controls interface."""

    def __init__(self, f_path: str):
        super().__init__()

        self.script_path = f_path
        self.init_madx(f_path)

        self.controls = {
            'BETA0': QCheckBox('BETA0'),
            'aperture': QGroupBox('Aperture'),
            'envelope': QGroupBox('Envelope'),
            'freeze': QGroupBox('Freeze'),
        }
        controls_aperture_layout = QHBoxLayout()
        controls_envelope_layout = QHBoxLayout()
        for dim in 'xy':
            widget = QCheckBox(dim.upper())
            widget.stateChanged.connect(partial(self._toggle_aperture, dim))
            controls_aperture_layout.addWidget(widget)

            widget = QCheckBox(dim.upper())
            widget.stateChanged.connect(partial(self._toggle_envelope, dim))
            controls_envelope_layout.addWidget(widget)
        self.controls['aperture'].setLayout(controls_aperture_layout)
        self.controls['envelope'].setLayout(controls_envelope_layout)

        controls_freeze_layout = QHBoxLayout()
        for what in ('twiss', 'orbit'):
            widget = QCheckBox(what.capitalize())
            widget.stateChanged.connect(partial(self._toggle_freeze, what))
            controls_freeze_layout.addWidget(widget)
        self.controls['freeze'].setLayout(controls_freeze_layout)

        controls_layout = QHBoxLayout()
        for widget in self.controls.values():
            controls_layout.addWidget(widget)
        controls_layout.addStretch(1)

        self.canvas = Canvas()
        self.toolbar = NavigationToolbar2QT(self.canvas, parent=self)

        self.beta0_input = Beta0Widget(on_value_changed=lambda x: self.update_plots())
        self.beta0_input.parse_beta0(f_path)
        self.beta0_input.setVisible(bool(self.beta0_input.arguments))
        self.controls['BETA0'].setCheckState(
            Qt.Checked if self.beta0_input.isVisible() else Qt.Unchecked)

        self.emittance_input = EmittanceWidget(on_value_changed=self.canvas.update_envelope)
        self.emittance_input.setVisible(False)

        main_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.beta0_input)
        main_layout.addWidget(self.emittance_input)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)
        self.setLayout(main_layout)

        aperture_data = {
            cmd['label'].lower(): cmd['arguments']['aperture']
            for cmd in find_all_commands(Path(f_path).read_text())
            if 'aperture' in cmd['arguments']
        }
        for label, aperture in aperture_data.items():
            if aperture.startswith('{'):
                assert aperture.endswith('}')
                ax, ay, *remainder = aperture[1:-1].split(',')
                if remainder:
                    raise RuntimeError(f'Aperture type for element {label!r} not supported '
                                       f'(must be circular or elliptical)')
            else:
                ax = ay = aperture
            aperture_data[label] = dict(x=float(ax), y=float(ay))

        twiss = self.compute_twiss()
        self.canvas.add_lattice(twiss)
        self.canvas.add_aperture(aperture_data, twiss)
        self.canvas.update_plots(twiss)
        self.canvas.update_envelope(self.emittance_input.data)

        self.controls_widget = ControlsWidget(
            twiss,
            update_callback=self.controls_changed_value,
            hover_callback=self.canvas.highlight_lattice_element)
        self.controls_widget.show()

        self.controls['BETA0'].stateChanged.connect(self._toggle_beta0)

    def init_madx(self, f_path):
        self.madx = Madx()
        self.madx.call(f_path)

    def compute_twiss(self):
        """Compute the Twiss table from the current MADX interpreter state (providing BETA0 if set)."""
        if self.controls['BETA0'].checkState() == Qt.Checked:
            beta0_args = self.beta0_input.arguments
        else:
            beta0_args = {}
        logger.info(f'Calling twiss with BETA0 args: {beta0_args!r}')
        return self.madx.twiss(**beta0_args)

    def update_plots(self):
        """Compute Twiss table and update plots in canvas accordingly."""
        try:
            self.canvas.update_plots(self.compute_twiss())
        except TwissFailed:
            self.canvas.twiss_failed()
            logger.info('Twiss failed')
        except RuntimeError:
            self.canvas.twiss_failed()
            self.init_madx(self.script_path)
            logger.info('MADX stopped working (restarted)')

    def controls_changed_value(self, name, attr, value):
        """Callback for value changes of parameters in the Controls widget.

        Whenever a parameter in the controls widget changes its value, this method should be called
        to enforce an update of the plots.

        Args:
            name: MADX label of the element which changed one of its attributes.
            attr: Name of the attribute which changed value.
            value: The attribute's new value in MADX units.
        """
        update_cmd = f'{name}->{attr} = {value:.10f};'
        logger.info(f'Update attribute value: {update_cmd!r}')
        self.madx.input(update_cmd)
        self.update_plots()

    def _toggle_freeze(self, which, state):
        """Freeze or unfreeze one of the plots.

        Args:
            which: Which plot to use ("twiss" or "orbit").
            state: Frozen or not.
        """
        getattr(self.canvas, f'toggle_freeze_{which}')(state == Qt.Checked)

    def _toggle_beta0(self, state):
        """Show or hide the BETA0 input widget."""
        state = (state == Qt.Checked)
        if state:
            self.beta0_input.parse_beta0(self.script_path)
        self.beta0_input.setVisible(state)

    def _toggle_aperture(self, dim, state):
        """Show or hide aperture in the orbit plot.

        Args:
            dim: Dimension for which aperture is toggled ("x" or "y").
            state: Visible or not.
        """
        logger.debug(f'Toggle aperture: {state}')
        self.canvas.toggle_aperture(dim, state == Qt.Checked)

    def _toggle_envelope(self, dim, state):
        """Show or hide envelope in the orbit plot.

        Args:
            dim: Dimension for which envelope is toggled ("x" or "y").
            state: Visible or not.
        """
        self.canvas.toggle_envelope(dim, state == Qt.Checked)
        self.emittance_input.setVisible(
            any(box.checkState() == Qt.Checked for box in self.controls['envelope'].findChildren(QCheckBox)))


class ControlsWidget(ConfigWidget):
    """Widget containing the controls for the various lattice parameter."""

    config = Namespace(
        kick_unit = 'mrad',
        kick_min = -1e3,
        kick_max =  1e3,
        kick_step_min = 0.01,
        kick_step_max = 1.0,
        kick_step_default = 0.1,
        k1_unit = '1/m^2',
        k1_min = -1e3,
        k1_max =  1e3,
        k1_step_min = 1e-5,
        k1_step_max = 1e-2,
        k1_step_default = 1e-3,
        filter_zero_strength_quadrupoles = False,
    )

    def __init__(self, twiss, *, update_callback, hover_callback):
        """Initializes the control widget from Twiss data and connects callbacks.

        Args:
            twiss: Twiss table as returned by `cpymad.Madx.twiss`.
            update_callback: Slot to be connected to each of the parameters' `valueChanged`.
                The parameter name and attribute is provided as well. I.e. the callback should have
                the following signature: `(name, attr, value)`.
            hover_callback: Slot to be connected to the parameters' `enterEvent` and `leaveEvent`.
                The parameter name is provided as well. I.e. the callback should have the following
                signature: `(name, hovering)`.
        """
        super().__init__()
        self.setWindowTitle('Controls')
        self.groups = {
            'hkicker': QGroupBox('HKicker'),
            'vkicker': QGroupBox('VKicker'),
            'quadrupole': QGroupBox('Quadrupole'),
        }
        self.units = {
            'hkicker': dict(factor=units_database[self.config.kick_unit], text=self.config.kick_unit),
            'vkicker': dict(factor=units_database[self.config.kick_unit], text=self.config.kick_unit),
            'quadrupole': dict(factor=units_database[self.config.k1_unit], text=self.config.k1_unit),
        }
        self.input_fields = defaultdict(dict)
        self.values = {}
        attributes = {
            'hkicker': 'kick',
            'vkicker': 'kick',
            'quadrupole': 'k1',
        }
        value_from_twiss = {
            'hkicker': lambda row: row['hkick'],
            'vkicker': lambda row: row['vkick'],
            'quadrupole': lambda row: row['k1l'] / row['l'],
        }
        group_layouts = {k: QVBoxLayout() for k in self.groups}
        for index in it.count():
            try:
                element = twiss[index]
            except IndexError:
                break
            name = get_label_from_twiss(element['name'])
            keyword = element['keyword'].lower()
            if self.config.filter_zero_strength_quadrupoles and keyword == 'quadrupole' and element['k1l'] == 0:
                continue
            if keyword in self.groups:
                def _on_value_changed(x, name=name, attr=attributes[keyword], factor=self.units[keyword]['factor']):
                    update_callback(name, attr, x / factor)

                value = value_from_twiss[keyword](element) / self.units[keyword]['factor']
                element_layout = QHBoxLayout()
                element_layout.addWidget(QLabel(name))
                field = QDoubleSpinBox()
                field.setRange(getattr(self.config, f'{attributes[keyword]}_min'),
                               getattr(self.config, f'{attributes[keyword]}_max'))
                field.setValue(value)
                field.valueChanged.connect(_on_value_changed)
                element_layout.addWidget(field)
                element_layout.addWidget(QLabel(self.units[keyword]['text']))
                widget = ControlsElement(name, element_layout, hover_callback=hover_callback)
                group_layouts[keyword].addWidget(widget)
                self.input_fields[keyword][name] = field
                self.units[name] = self.units[keyword]

        for keyword, layout in group_layouts.items():
            def _on_value_changed(x, group=keyword):
                for field in self.input_fields[group].values():
                    field.setSingleStep(10**-x)

            slider = LabeledHSlider(int(-math.log10(getattr(self.config, f'{attributes[keyword]}_step_max'))),
                                    int(-math.log10(getattr(self.config, f'{attributes[keyword]}_step_min'))))
            for field in self.input_fields[keyword].values():
                field.setDecimals(slider.maximum())
            slider.valueChanged.connect(_on_value_changed)
            slider.setValue(-math.log10(getattr(self.config, f'{attributes[keyword]}_step_default')))
            slider_layout = QHBoxLayout()
            slider_label = QLabel('Decimal step size:')
            slider_label.setAlignment(Qt.AlignTop)
            slider_layout.addWidget(slider_label)
            slider_layout.addWidget(slider)
            slider_layout.addStretch(1)
            layout.insertLayout(0, slider_layout)  # Insert at the top of the group.

        for key, group in self.groups.items():
            group_layouts[key].addStretch(1)
            group.setLayout(group_layouts[key])

        kicker_layout = QVBoxLayout()
        kicker_layout.addWidget(self.groups['hkicker'])
        kicker_layout.addWidget(self.groups['vkicker'])

        main_layout = QHBoxLayout()
        main_layout.addLayout(kicker_layout)
        main_layout.addWidget(self.groups['quadrupole'])

        wrapper_widget = QWidget()
        wrapper_widget.setLayout(main_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidget(wrapper_widget)
        tmp_layout = QHBoxLayout()
        tmp_layout.addWidget(scroll_area)
        self.setLayout(tmp_layout)


class ControlsElement(QWidget):
    """An element of the controls widget with support for hovering events."""

    def __init__(self, name, layout, *, hover_callback):
        super().__init__()
        self.name = name
        self.hover_callback = hover_callback
        self.setLayout(layout)

    def enterEvent(self, event):
        self.hover_callback(self.name, True)

    def leaveEvent(self, event):
        self.hover_callback(self.name, False)


class Beta0Widget(ConfigWidget):
    """Widget controlling the BETA0 inputs."""

    config = Namespace(
        decimals = 5,
        step_size = 1e-5,
        min = -1e9,
        max =  1e9,
    )

    def __init__(self, *, on_value_changed):
        """Initialize the widget with a callback for its input fields.

        Args:
            on_value_changed: Callback to be connected to each input field's `valueChanged` signal.
        """
        super().__init__()
        self.beta0_input = {
            'X': QDoubleSpinBox(),
            'Y': QDoubleSpinBox(),
            'BETX': QDoubleSpinBox(),
            'BETY': QDoubleSpinBox(),
            'ALFX': QDoubleSpinBox(),
            'ALFY': QDoubleSpinBox(),
            'DX': QDoubleSpinBox(),
            'DY': QDoubleSpinBox(),
            'DPX': QDoubleSpinBox(),
            'DPY': QDoubleSpinBox(),
        }
        layout = QHBoxLayout()
        layout.addWidget(QLabel('BETA0:'))
        for label, widget in self.beta0_input.items():
            layout.addWidget(QLabel(f'{label}:'))
            widget.setRange(self.config.min, self.config.max)
            widget.setDecimals(self.config.decimals)
            widget.setSingleStep(self.config.step_size)
            widget.valueChanged.connect(on_value_changed)
            layout.addWidget(widget)
        layout.addStretch(1)
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(layout)
        scroll_area = QScrollArea()
        scroll_area.setWidget(wrapper_widget)
        main_layout = QHBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    @property
    def arguments(self):
        return {k.lower(): v.value() for k, v in self.beta0_input.items() if v.value() != 0}

    def parse_beta0(self, f_path: str):
        """Parse 'BETA0' command from the given file which must be placed on its own line."""
        text = Path(f_path).read_text()
        try:
            beta0 = next(find_all_commands(text, keyword='beta0'))
        except StopIteration:
            logger.info(f'No BETA0 command found in {f_path!r}')
            return
        for widget in self.beta0_input.values():
            widget.clear()
        for name, value in beta0['arguments'].items():
            input_field = self.beta0_input[name.upper()]
            value = float(value)
            input_field.setValue(value)


class EmittanceWidget(ConfigWidget):
    """Widget controlling the emittance input."""

    config = Namespace(
        decimals = 2,
        step_size = 1e-2,
        min = 0,
        max = 1e9,
        units = 'm*rad',
    )

    def __init__(self, *, on_value_changed):
        """Initialize the widget with a callback for its input fields.

        Args:
            on_value_changed: Callback to be connected to each input field's signal indicating a change
                of the corresponding value. The callback receives the full emittance data as a dictionary,
                i.e. `{"gamma": ..., "emitx": ..., "emity": ...}`.
        """
        super().__init__()
        self.input_fields = {
            'gamma': QLineEdit(),
            'emitx': QDoubleSpinBox(),
            'emity': QDoubleSpinBox(),
        }
        for key in ('emitx', 'emity'):
            self.input_fields[key].setRange(self.config.min, self.config.max)
            self.input_fields[key].setDecimals(self.config.decimals)
            self.input_fields[key].setSingleStep(self.config.step_size)
            self.input_fields[key].setValue(0)
            self.input_fields[key].valueChanged.connect(lambda x: on_value_changed(self.data))
        validator = QDoubleValidator()
        validator.setRange(self.config.min, self.config.max)
        self.input_fields['gamma'].setValidator(validator)
        self.input_fields['gamma'].setText('1.0')
        self.input_fields['gamma'].editingFinished.connect(lambda: on_value_changed(self.data))
        labels = {
            'gamma': '\N{GREEK SMALL LETTER GAMMA}',
            'emitx': '\N{GREEK SMALL LETTER EPSILON}x',
            'emity': '\N{GREEK SMALL LETTER EPSILON}y',
        }
        units_ids = {
            'gamma': None,
            'emitx': self.config.units,
            'emity': self.config.units,
        }
        self.units = {}
        layout = QHBoxLayout()
        layout.addWidget(QLabel('Emittance: '))
        for key, field in self.input_fields.items():
            layout.addWidget(QLabel(f'{labels[key]}:'))
            layout.addWidget(field)
            self.units[key] = units_database[units_ids[key]]
            if units_ids[key] is not None:
                layout.addWidget(QLabel(f'[{convert_ascii_math_to_unicode(units_ids[key])}]'))
        layout.addStretch(1)
        self.setLayout(layout)

    @property
    def data(self):
        data = {'gamma': float(self.input_fields['gamma'].text())}  # Gamma is unitless.
        for key in ('emitx', 'emity'):
            data[key] = self.input_fields[key].value() / self.units[key]
        return data


class Canvas(ConfigWidget, FigureCanvasQTAgg):
    """The Canvas Widget containing the various plots and lattice sketch."""

    config = Namespace(
        figsize_inches = (14, 12),
        gridspec_height_ratios = (1, 5, 5),
        display_unit_twiss = 'm',
        display_unit_orbit = 'mm',
        color_x = '#1f77b4',
        color_y = '#ff7f0e',
        color_kicker = 'firebrick',
        color_quadrupole = 'cornflowerblue',
        color_sextupole = 'limegreen',
        color_bend = 'gold',
        color_default = 'lightgrey',
        color_default_alpha = 0.2,
        lattice_min_length_factor = 1e-3,
        max_aper_padding_factor = 1.2,
        aper_min_length_factor = 5e-4,
        aper_color_alpha = 0.5,
        envelope_color_alpha = 0.4,
        lattice_height = 1.0,
        lattice_alpha = 0.7,
        lattice_height_highlight = 1.5,
        lattice_alpha_highlight = 1.0,
        freeze_color_alpha = 0.7,
        freeze_line_style = '--',
        display_zero_strength_quadrupoles_as_drifts = False,
    )

    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.fig.set_size_inches(self.config.figsize_inches)
        self.ax_lattice, self.ax_twiss, self.ax_orbit = self.fig.subplots(
            nrows=3, sharex=True, gridspec_kw={'height_ratios': self.config.gridspec_height_ratios})
        self.ax_twiss.set_ylabel(f'Beta functions [{self.config.display_unit_twiss}]')
        self.ax_orbit.set_xlabel('s [m]')
        self.ax_orbit.set_ylabel(f'Beam position [{self.config.display_unit_orbit}]')
        self.units = {
            'twiss': units_database[self.config.display_unit_twiss],
            'orbit': units_database[self.config.display_unit_orbit],
        }

        for ax in (self.ax_twiss, self.ax_orbit):
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
        self.ax_lattice.set_ylim([0, 1.5])
        self.ax_lattice.axis('off')

        self.beta = {
            'x': self.ax_twiss.plot([], [], self.config.color_x, label=r'$\beta_X$')[0],
            'y': self.ax_twiss.plot([], [], self.config.color_y, label=r'$\beta_Y$')[0],
        }
        self.ax_twiss.legend()

        self.orbit = {
            'x': self.ax_orbit.plot([], [], self.config.color_x, label='X')[0],
            'y': self.ax_orbit.plot([], [], self.config.color_y, label='Y')[0],
        }
        self.ax_orbit.legend()

        self.twiss_failed_text = [
            self.ax_twiss.text(0, 0, 'Twiss failed', fontdict=dict(fontweight='bold', fontsize=24, color='firebrick')),
            self.ax_orbit.text(0, 0, 'Twiss failed', fontdict=dict(fontweight='bold', fontsize=24, color='firebrick')),
        ]
        for text in self.twiss_failed_text:
            text.set_visible(False)

        self.colors_xy = dict(x=self.config.color_x, y=self.config.color_y)
        self.keyword_colors = defaultdict(
            lambda: (self.config.color_default, self.config.color_default_alpha),
            hkicker=(self.config.color_kicker, self.config.lattice_alpha),
            vkicker=(self.config.color_kicker, self.config.lattice_alpha),
            kicker=(self.config.color_kicker, self.config.lattice_alpha),
            quadrupole=(self.config.color_quadrupole, self.config.lattice_alpha),
            sextupole=(self.config.color_sextupole, self.config.lattice_alpha),
            sbend=(self.config.color_bend, self.config.lattice_alpha),
            rbend=(self.config.color_bend, self.config.lattice_alpha),
        )

        self.aperture = {}
        self.envelope = {}
        self.frozen = {'twiss': dict(), 'orbit': dict()}
        self.lattice_elements = {}
        self._envelope_data = None

    def add_lattice(self, twiss):
        """Add a lattice layout sketch from provided Twiss data.

        Args:
            twiss: Twiss table as returned by `cpymad.Madx.twiss`.
        """
        min_length = self.config.lattice_min_length_factor * twiss['s'].max()
        pos = 0
        for index in range(1, len(twiss['s']) - 1):  # Skip "#S" and "#E" markers.
            element = twiss[index]
            keyword = element['keyword'].lower()
            if self.config.display_zero_strength_quadrupoles_as_drifts and keyword == 'quadrupole' and element['k1l'] == 0:
                keyword = 'drift'
            label = get_label_from_twiss(element['name'])
            s = element['s']
            length = max(s - pos, min_length)
            color, alpha = self.keyword_colors[keyword]
            self.lattice_elements[label] = self.ax_lattice.bar(
                pos, self.config.lattice_height, length, 0.0,
                align='edge', color=color, alpha=alpha,
            )
            pos = s
        self.draw()

    def add_aperture(self, aperture_data, twiss):
        """Add aperture to the orbit plot from provided aperture and Twiss data.

        Args:
            aperture_data: Dictionary mapping element labels to aperture data in the form
                `{label: {"x": ..., "y": ...}, ...}`.
            twiss: Twiss table as returned by `cpymad.Madx.twiss`.
        """
        if not aperture_data:
            logger.info('Cannot add aperture, no aperture data was provided')
            return
        min_length = self.config.aper_min_length_factor * twiss['s'].max()
        element_labels = [get_label_from_twiss(x) for x in twiss['name']]
        aper = {dim: [ap[dim] for ap in aperture_data.values()] for dim in 'xy'}
        top_aper = self.config.max_aper_padding_factor * max(max(ap) for ap in aper.values())
        start_pos = [twiss['s'][i-1] for i in map(element_labels.index, aperture_data)]
        length = [max(twiss['s'][i] - twiss['s'][i-1], min_length)
                  for i in map(element_labels.index, aperture_data)]
        factor = self.units['orbit']
        for dim in 'xy':
            self.aperture[dim] = self.ax_orbit.bar(  # First upper then lower part.
                start_pos * 2,
                [(top_aper - ap)*factor for ap in aper[dim]] * 2,
                length * 2,
                [ap*factor for ap in aper[dim]] + [-top_aper*factor]*len(aper[dim]),
                align='edge',
                color=self.colors_xy[dim], alpha=self.config.aper_color_alpha,
            )
            for artist in self.aperture[dim]:
                artist.set_visible(False)

    def draw(self):
        for ax in (self.ax_twiss, self.ax_orbit):
            ax.relim()
            ax.autoscale_view()
        super().draw()

    def update_envelope(self, data):
        """Update the envelope in the orbit plot with the provided emittance data.

        Args:
            data: Emittance data as returned by `EmittanceWidget.data`.
        """
        for dim in 'xy':
            try:
                old_envelope = self.envelope[dim]
            except KeyError:
                was_visisble = False
            else:
                was_visisble = old_envelope.get_visible()
                self.ax_orbit.collections.remove(old_envelope)

            envelope = np.sqrt(data[f'emit{dim}'] * self.beta[dim].get_ydata() / data['gamma'])

            self.envelope[dim] = self.ax_orbit.fill_between(
                self.orbit[dim].get_xdata(),
                self.orbit[dim].get_ydata() - envelope,
                self.orbit[dim].get_ydata() + envelope,
                color=self.colors_xy[dim], alpha=self.config.envelope_color_alpha,
            )
            self.envelope[dim].set_visible(was_visisble)
        self._envelope_data = data
        self.draw()

    def toggle_envelope(self, dim, visible):
        self.envelope[dim].set_visible(visible)
        self.draw()

    def update_plots(self, twiss):
        """Update Twiss and orbit plots from the provided Twiss data.

        Args:
            twiss: Twiss table as returned by `cpymad.Madx.twiss`.
        """
        logger.debug('Update plots')
        for text in self.twiss_failed_text:
            text.set_visible(False)
        for dim in 'xy':
            self.beta[dim].set_xdata(twiss.s)
            self.beta[dim].set_ydata(twiss[f'bet{dim}'] * self.units['twiss'])
            self.beta[dim].set_visible(True)

            self.orbit[dim].set_xdata(twiss.s)
            self.orbit[dim].set_ydata(twiss[dim] * self.units['orbit'])
            self.orbit[dim].set_visible(True)

        if self._envelope_data is not None:
            self.update_envelope(self._envelope_data)  # This calls `self.draw` already.
        else:
            self.draw()

    def twiss_failed(self):
        for dim in 'xy':
            self.beta[dim].set_visible(False)
            self.orbit[dim].set_visible(False)
        for text in self.twiss_failed_text:
            text.set_visible(True)
        self.draw()

    def highlight_lattice_element(self, label, highlight):
        """Highlight lattice element in the lattice layout sketch.

        Args:
            label: Label of the element.
            highlight: Whether to highlight or not.
        """
        logger.debug(f'Highlight lattice element: {label} -> {highlight}')
        element = self.lattice_elements[label][0]
        if highlight:
            element.set_height(self.config.lattice_height_highlight)
            element.set_alpha(self.config.lattice_alpha_highlight)
            self.ax_lattice.set_title(label)
        else:
            element.set_height(self.config.lattice_height)
            element.set_alpha(self.config.lattice_alpha)
            self.ax_lattice.set_title('')
        self.draw()

    def toggle_aperture(self, dim, visible: bool):
        for artist in self.aperture[dim]:
            artist.set_visible(visible)
        self.ax_orbit.relim()
        self.ax_orbit.autoscale_view()
        self.draw()

    def toggle_freeze_twiss(self, freeze: bool):
        self.toggle_freeze(self.ax_twiss, self.beta, self.frozen['twiss'], freeze)

    def toggle_freeze_orbit(self, freeze: bool):
        self.toggle_freeze(self.ax_orbit, self.orbit, self.frozen['orbit'], freeze)

    def toggle_freeze(self, ax, plots, frozen_dict, freeze: bool):
        """Freeze either Twiss or orbit data in the plots.

        Args:
            ax: The axis on which to freeze.
            plots: The artists which need to be frozen in a dictionary mapping from dimension to artist.
            frozen_dict: Previously frozen artists in a dictionary mapping from dimension to artist.
            freeze: Whether to freeze or not.
        """
        logger.debug(f'Freezing {ax}: {freeze}')
        for artist in frozen_dict.values():
            artist.remove()
        frozen_dict.clear()
        if freeze:
            for dim, artist in plots.items():
                frozen_dict[dim] = ax.plot(
                    artist.get_xdata(), artist.get_ydata(),
                    self.config.freeze_line_style,
                    color=self.colors_xy[dim], alpha=self.config.freeze_color_alpha,
                )[0]
        self.draw()


def get_label_from_twiss(label):
    return label.rsplit(':', 1)[0]


def convert_ascii_math_to_unicode(text):
    return text.replace('*', '\N{MIDDLE DOT}')


units_database = {  # Factors for converting from SI to the given unit.
    'm': 1.0,
    'mm': 1e3,
    'mrad': 1e3,
    '1/m^2': 1.0,
    'm*rad': 1.0,
    'mm*mrad': 1e6,
    None: 1.0,  # Unitless quantities.
}
