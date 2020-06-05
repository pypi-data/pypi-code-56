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

# Here follows a plea in German to keep the comments in English so
# that you may understand them, dear visitor ...
#
# Meine Kommentare in den Quellcodes sind absichtlich auf Englisch
# gehalten, damit Leute, die im Internet nach Lösungen suchen, den
# Code nachvollziehen können.  Daher bitte ich darum, zusätzliche
# Kommentare ebenfalls auf Englisch zu schreiben.  Vielen Dank!


from gi.repository import Gtk, Gdk

import os

from .locale import _
from .settings import *


DISTANCE_LAYOUT_BLOCKS = 5


def SpinButton(label_text, varname, value=0, lower=0, upper=0, 
               step_incr=0, page_incr=0, page_size=0):
    hbox = Gtk.HBox(False, DISTANCE_LAYOUT_BLOCKS)

    label = Gtk.Label(label_text)
    label.set_alignment(0, 0.5)
    hbox.pack_start(label, False, True, 0)

    adj = Gtk.Adjustment(value, lower, upper, step_incr, page_incr, page_size)
    spinner = Gtk.SpinButton.new(adj, 0, 0)
    spinner.set_numeric(True)
    spinner.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
    hbox.pack_start(spinner, False, True, 0)
    return hbox, spinner


class SettingsDialog():

    def __init__(self, app, parent):
        self.app = app
        win = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        win.set_title(_("OSD Neo2 Settings"))

        # Tell the window manager to no activate the window and to no
        # add it to the dock, ...
        win.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        win.set_position(Gtk.WindowPosition.MOUSE)
        win.set_transient_for(parent)
        # This is required to avoid the dialog is slipping below the
        # main window
        win.set_keep_above(True)

        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        win.add(notebook)

        # -- Display Options page ---

        vbox = Gtk.VBox(False, 0)
        vbox.set_border_width(DISTANCE_LAYOUT_BLOCKS)
        notebook.append_page(vbox, Gtk.Label(_("Display options")))

        for name, varname in (
                (_("Display _Main Keyboard"), 'display_main_keyboard'),
                (_("Display _Numeric Keyboard"), 'display_numeric_keyboard'),
                (_("on all Desktops"), 'appear_on_all_desktops'),
                ):
            button = Gtk.CheckButton(name, use_underline=True)
            button.connect("toggled", app.on_bool_settings_response, varname)
            button.set_active(getattr(app, varname))
            vbox.pack_start(button, True, True, 0)


        # :``magnification_in_percent``:
        current_value = getattr(app, 'magnification')
        box, spinner = SpinButton(_("Magnification:"), 'magnification_in_percent',
                                  current_value, 25, 500, 25)
        spinner.connect('value-changed', self.do_value_changed,
                        'magnification', 'magnification_in_percent')
        label = Gtk.Label(_("%"))
        box.pack_start(label, False, True, 0)
        vbox.pack_start(box, True, True, DISTANCE_LAYOUT_BLOCKS)

        # selected_keyboard_type
        hbox2 = Gtk.HBox(False, 0)
        vbox.pack_start(hbox2, True, True, 0)

        label = Gtk.Label(_("Keyboard Type:"))
        label.set_alignment(0, 0.5)
        hbox2.pack_start(label, False, False, 0)

        current_value = getattr(app, 'keyboard_type')
        combobox = Gtk.ComboBoxText()
        self.__keyboard_types = []
        for name, value in (
                (_("PC 105"), 'pc105'),
                (_("ErgoDox"), 'ergodox'),
                ):
            combobox.append_text(name)
            self.__keyboard_types.append(value)
        combobox.set_active(self.__keyboard_types.index(current_value))
        combobox.connect('changed', self.on_keyboard_type_changed)
        hbox2.pack_start(combobox, False, True, 0)


        # -- Advanced Options page ---

        vbox = Gtk.VBox(False, 0)
        vbox.set_border_width(DISTANCE_LAYOUT_BLOCKS)
        notebook.append_page(vbox, Gtk.Label(_("Advanced")))

        # selected_keyboard_driver
        vbox2 = Gtk.VBox(False, 0)
        vbox.pack_start(vbox2, True, True, 0)

        label = Gtk.Label(_("Keyboard Driver:"))
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, False, 0)

        label = Gtk.Label(_("(changing requires restart)"))
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, False, 0)

        current_value = getattr(app, 'keyboard_driver')
        combobox = Gtk.ComboBoxText()
        self.__keyboard_drivers = []
        for name, value in (
                (_("xkbdmap (recommended)"), 'xkbdmap'),
                (_("xmodmap"), 'xmodmap'),
                ):
            combobox.append_text(name)
            self.__keyboard_drivers.append(value)
        combobox.set_active(self.__keyboard_drivers.index(current_value))
        combobox.connect('changed', self.on_keyboard_driver_changed)
        vbox2.pack_start(combobox, False, True, 0)

        vbox.pack_start(Gtk.HSeparator(), True, True, 0)

        # polling_in_milliseconds
        vbox2 = Gtk.VBox(False, 0)
        vbox.pack_start(vbox2, True, True, 0)

        current_value = getattr(app, 'polling')
        box, spinner = SpinButton(_("Polling intverval:"), 'polling_in_milliseconds',
                                  current_value, 25, 500, 25)
        spinner.connect('value-changed', self.do_value_changed,
                        'polling', 'polling_in_milliseconds')
        label = Gtk.Label(_("ms"))
        box.pack_start(label, False, True, 0)
        vbox2.pack_start(box, False, True, 0)

        label = Gtk.Label(_("Default: %s ms") % DEFAULT_POLLING_INTERVAL)
        label.set_alignment(1, 0)
        vbox2.pack_start(label, True, True, DISTANCE_LAYOUT_BLOCKS)

        self._pollig_vbox = vbox2
        self._pollig_vbox.set_sensitive(
            getattr(app, 'keyboard_driver') == 'xmodmap')

        win.show_all()


    def do_value_changed(self, widget, attrname, varname):
        value = widget.get_value_as_int()
        setattr(self.app, attrname, value)
        settings.set('settings', varname, value)
        self.app.update_display()
        return True


    def on_keyboard_driver_changed(self, combobox):
        index = combobox.get_active()
        value = self.__keyboard_drivers[index]
        attrname = 'keyboard_driver'
        varname = 'selected_keyboard_driver'
        setattr(self.app, attrname, value)
        settings.set('settings', varname, value)
        self._pollig_vbox.set_sensitive(value == 'xmodmap')
        self.app.update_display()
        return True


    def on_keyboard_type_changed(self, combobox):
        index = combobox.get_active()
        value = self.__keyboard_types[index]
        attrname = 'keyboard_type'
        varname = 'keyboard_type'
        setattr(self.app, attrname, value)
        settings.set('settings', varname, value)
        self.app.update_display()
        return True
