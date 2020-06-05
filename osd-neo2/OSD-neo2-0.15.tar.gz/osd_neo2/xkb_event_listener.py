# -*- coding: utf-8 -*-

"""
OSD Neo2
========
On screen display for learning the keyboard layout Neo2

Copyright (c) 2017-2020 Hartmut Goebel (http://crazy-compilers.com/)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Thank you for using free software!

This module implements a Xkb event listening loop thread.
"""


import threading

from . import simple_xkb_wrapper as xkb

class EventListener(threading.Thread):

    def __init__(self, app):
        self.app = app
        self.STOP = False
        super(EventListener, self).__init__()

    def run(self):
        app = self.app # shortcut
        self.STOP = False
        self.start_listen()

        while True:
            # Wait for some Xkb event to arrive
            event = xkb.XNextEvent(app.display_handle)
            if self.STOP:
                break
            if not event.xkb_type == xkb.XkbStateNotify:
                # we only handle state notify
                continue
            new_mod_states = xkb.ExtractLocks(event)

            # We only have to update the main window if the modifier
            # states have changed
            if new_mod_states != app.mod_states:
                app.mod_states = new_mod_states
                app.set_current_modifier()

        self.stop_listen()


    def stop(self):
        self.STOP = True
        # Make sure the listener gets events (which may be disabled
        # e.g. since the window is iconified)
        self.start_listen()
        # Send some event to unblock XNextEvent()
        xkb.XkbBellEvent(self.app.display_handle, None, -100, 0)
        xkb.XFlush(self.app.display_handle)


    def start_listen(self):
        # Listen to 'state notify' and 'bell' events. The bell events
        # are used to unblock XNextEvent() when the listener should
        # stop.
        xkb.XkbSelectEvents(self.app.display_handle,
                            xkb.XkbUseCoreKbd,  # select the core keyboard
                            xkb.XkbStateNotifyMask+xkb.XkbBellNotifyMask,
                            xkb.XkbStateNotifyMask+xkb.XkbBellNotifyMask)


    def stop_listen(self):
        xkb.XkbSelectEvents(self.app.display_handle,
                            xkb.XkbUseCoreKbd,  # select the core keyboard
                            xkb.XkbAllEventsMask, 0)
