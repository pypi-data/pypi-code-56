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
import json

from openlp.core.common.registry import Registry
from openlp.core.common.httputils import get_web_page
from openlp.core.common.mixins import RegistryProperties


class Poller(RegistryProperties):
    """
    Accessed by the web layer to get status type information from the application
    """
    def __init__(self):
        """
        Constructor for the poll builder class.
        """
        super(Poller, self).__init__()
        self.live_cache = None
        self.stage_cache = None
        self.chords_cache = None
        settings = Registry().get('settings_thread')
        self.address = settings.value('api/ip address')
        self.ws_port = settings.value('api/websocket port')
        self.http_port = settings.value('api/port')

    def raw_poll(self):
        return {
            'service': self.service_manager.service_id,
            'slide': self.live_controller.selected_row or 0,
            'item': self.live_controller.service_item.unique_identifier if self.live_controller.service_item else '',
            'twelve': self.settings.value('api/twelve hour'),
            'blank': self.live_controller.blank_screen.isChecked(),
            'theme': self.live_controller.theme_screen.isChecked(),
            'display': self.live_controller.desktop_screen.isChecked(),
            'version': 3,
            'isSecure': self.settings.value('api/authentication enabled'),
            'isAuthorised': False,
            'chordNotation': self.settings.value('songs/chord notation'),
            'isStageActive': self.is_stage_active(),
            'isLiveActive': self.is_live_active(),
            'isChordsActive': self.is_chords_active()
        }

    def poll(self):
        """
        Poll OpenLP to determine the current slide number and item name.
        """
        return {'results': self.raw_poll()}

    def main_poll(self):
        """
        Poll OpenLP to determine the current slide count.
        """
        result = {
            'slide_count': self.live_controller.slide_count
        }
        return json.dumps({'results': result}).encode()

    def reset_cache(self):
        """
        Reset the caches as the web has changed
        :return:
        """
        self.stage_cache = None
        self.live_cache = None
        self.chords.cache = None

    def is_stage_active(self):
        """
        Is stage active - call it and see but only once
        :return: if stage is active or not
        """
        if self.stage_cache is None:
            try:
                page = get_web_page(f'http://{self.address}:{self.http_port}/stage')
            except Exception:
                page = None
            if page:
                self.stage_cache = True
            else:
                self.stage_cache = False
        return self.stage_cache

    def is_live_active(self):
        """
        Is main active - call it and see but only once
        :return: if live is active or not
        """
        if self.live_cache is None:
            try:
                page = get_web_page(f'http://{self.address}:{self.http_port}/main')
            except Exception:
                page = None
            if page:
                self.live_cache = True
            else:
                self.live_cache = False
        return self.live_cache

    def is_chords_active(self):
        """
        Is chords active - call it and see but only once
        :return: if live is active or not
        """
        if self.chords_cache is None:
            try:
                page = get_web_page(f'http://{self.address}:{self.http_port}/chords')
            except Exception:
                page = None
            if page:
                self.chords_cache = True
            else:
                self.chords_cache = False
        return self.chords_cache
