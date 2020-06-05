# -*- coding: utf-8 -*-
"""
OSD Neo2
========
On screen display for learning the keyboard layout Neo2

Copyright (c) 2009-2010 Martin Zuther (http://www.mzuther.de/)
Copyright (c) 2015-2020 Hartmut Goebel (http://crazy-compilers.com/)

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

"""


from gi.repository import Gtk

from .locale import _

class StatusIcon:
    def __init__(self, app, image_filename, visible=True):
        icon = Gtk.StatusIcon.new_from_file(image_filename)
        self.icon = icon
        icon.set_visible(visible)
        icon.connect('popup-menu', self.on_right_click)
        icon.connect('activate', self.on_left_click)
        self.app = app

    def show(self): self.icon.set_visible(True)
    def hide(self): self.icon.set_visible(False)

    def open_app(self, event):
        self.app.do_deiconify()
        return True

    def close_app(self, event):
        self.app.do_quit()
        return True

    def open_settings(self, event):
        self.app.on_open_settings_dialog(None)
        return True

    def _make_menu(self, event_button, event_time, data=None):
        menu = Gtk.Menu()
        for name, func  in (
                (_("Settings …"), self.open_settings),
                (_("Show Keymap"), self.open_app),
                (_("Quit"), self.close_app),
                ):
            item = Gtk.MenuItem(name, use_underline=True)
            item.connect("activate", func)
            #item.connect_object("activate", func)
            menu.append(item)
        menu.show_all()

        #Popup the menu
        menu.popup(None, None, None, None, event_button, event_time)


    def on_right_click(self, data, event_button, event_time):
        self._make_menu(event_button, event_time)
        return True

    def on_left_click(self, event):
        self.open_app(event)
        return True
