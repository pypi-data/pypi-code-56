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
"""
Package to test the openlp.core.ui.advancedtab package.
"""
from openlp.core.ui.advancedtab import AdvancedTab
from openlp.core.ui.settingsform import SettingsForm


def test_creation(settings):
    """
    Test that Advanced Tab is created.
    """
    # GIVEN: A new Advanced Tab
    settings_form = SettingsForm(None)

    # WHEN: I create an advanced tab
    advanced_tab = AdvancedTab(settings_form)

    # THEN:
    assert "Advanced" == advanced_tab.tab_title, 'The tab title should be Advanced'


def test_change_search_as_type(settings):
    """
    Test that when search as type is changed custom and song configs are updated
    """
    # GIVEN: A new Advanced Tab
    settings_form = SettingsForm(None)
    advanced_tab = AdvancedTab(settings_form)

    # WHEN: I change search as type check box
    advanced_tab.on_search_as_type_check_box_changed(True)

    # THEN: we should have two post save processed to run
    assert 2 == len(settings_form.processes), 'Two post save processes should be created'
    assert "songs_config_updated" in settings_form.processes, 'The songs plugin should be called'
    assert "custom_config_updated" in settings_form.processes, 'The custom plugin should be called'
