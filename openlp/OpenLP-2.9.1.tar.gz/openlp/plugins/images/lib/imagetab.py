# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2020 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

from PyQt5 import QtWidgets

from openlp.core.common.i18n import UiStrings, translate
from openlp.core.lib.settingstab import SettingsTab
from openlp.core.widgets.buttons import ColorButton


class ImageTab(SettingsTab):
    """
    ImageTab is the images settings tab in the settings dialog.
    """
    def setup_ui(self):
        self.setObjectName('ImagesTab')
        super(ImageTab, self).setup_ui()
        self.background_color_group_box = QtWidgets.QGroupBox(self.left_column)
        self.background_color_group_box.setObjectName('background_color_group_box')
        self.form_layout = QtWidgets.QFormLayout(self.background_color_group_box)
        self.form_layout.setObjectName('form_layout')
        self.color_layout = QtWidgets.QHBoxLayout()
        self.background_color_label = QtWidgets.QLabel(self.background_color_group_box)
        self.background_color_label.setObjectName('background_color_label')
        self.color_layout.addWidget(self.background_color_label)
        self.background_color_button = ColorButton(self.background_color_group_box)
        self.background_color_button.setObjectName('background_color_button')
        self.color_layout.addWidget(self.background_color_button)
        self.form_layout.addRow(self.color_layout)
        self.information_label = QtWidgets.QLabel(self.background_color_group_box)
        self.information_label.setObjectName('information_label')
        self.information_label.setWordWrap(True)
        self.form_layout.addRow(self.information_label)
        self.left_layout.addWidget(self.background_color_group_box)
        self.left_layout.addStretch()
        self.right_column.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.right_layout.addStretch()
        # Signals and slots
        self.background_color_button.colorChanged.connect(self.on_background_color_changed)

    def retranslate_ui(self):
        self.background_color_group_box.setTitle(UiStrings().BackgroundColor)
        self.background_color_label.setText(UiStrings().BackgroundColorColon)
        self.information_label.setText(
            translate('ImagesPlugin.ImageTab', 'Visible background for images with aspect ratio different to screen.'))

    def on_background_color_changed(self, color):
        self.background_color = color

    def load(self):
        self.settings.beginGroup(self.settings_section)
        self.background_color = self.settings.value('background color')
        self.initial_color = self.background_color
        self.settings.endGroup()
        self.background_color_button.color = self.background_color

    def save(self):
        self.settings.beginGroup(self.settings_section)
        self.settings.setValue('background color', self.background_color)
        self.settings.endGroup()
        if self.initial_color != self.background_color:
            self.settings_form.register_post_process('images_config_updated')
