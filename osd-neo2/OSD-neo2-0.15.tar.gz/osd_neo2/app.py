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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from gi.repository import GObject

import os

from . import package_path
from .locale import _
from . import simple_xkb_wrapper as xkb, statusicon, xkb_event_listener
from .settings import *

# specifies distance between main keyboard and numeric keyboard (in pixels)
DISTANCE_LAYOUT_BLOCKS = 10

class OSDneo2:
    layers = {}
    # layer matrix for "xkbdmap" with disabled Locks (plain)
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        1 |       4 |
    # | Mod3 on   |        3 |       6 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        2 |       0 |
    # | Mod3 on   |        5 |       0 |
    # |-----------+----------+---------|
    layers['xkbdmap', 'plain'] = {
        '   ': 1,
        ' 3 ': 3,
        '  4': 4,
        ' 34': 6,
        'S  ': 2,
        'S3 ': 5,
        'S 4': 0,
        'S34': 0,
    }
    # layer matrix for "xkbdmap" with enabled Caps Lock
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        7 |       4 |
    # | Mod3 on   |        3 |       6 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        8 |       0 |
    # | Mod3 on   |        5 |       0 |
    # |-----------+----------+---------|
    layers['xkbdmap', 'caps_lock'] = {
        '   ': 7,
        ' 3 ': 3,
        '  4': 4,
        ' 34': 6,
        'S  ': 8,
        'S3 ': 5,
        'S 4': 0,
        'S34': 0,
    }
    # layer matrix for "xkbdmap" with enabled Mod4 Lock
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        4 |       1 |
    # | Mod3 on   |        6 |       3 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        0 |       2 |
    # | Mod3 on   |        0 |       5 |
    # |-----------+----------+---------|
    layers['xkbdmap', 'mod4_lock'] = {
        '   ': 4,
        ' 3 ': 6,
        '  4': 1,
        ' 34': 3,
        'S  ': 0,
        'S3 ': 0,
        'S 4': 2,
        'S34': 5,
    }
    # layer matrix for "xkbdmap" with enabled Caps+Mod4 Lock
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        4 |       7 |
    # | Mod3 on   |        6 |       3 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        0 |       8 |
    # | Mod3 on   |        0 |       5 |
    # |-----------+----------+---------|
    layers['xkbdmap', 'caps_mod4_lock'] = {
        '   ': 4,
        ' 3 ': 6,
        '  4': 7,
        ' 34': 3,
        'S  ': 0,
        'S3 ': 0,
        'S 4': 8,
        'S34': 5,
    }
    # layer matrix for "xmodmap" with disabled Locks (plain)
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        1 |       4 |
    # | Mod3 on   |        3 |       6 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        2 |       0 |
    # | Mod3 on   |        5 |       6 |
    # |-----------+----------+---------|
    layers['xmodmap', 'plain'] = {
        '   ': 1,
        ' 3 ': 3,
        '  4': 4,
        ' 34': 6,
        'S  ': 2,
        'S3 ': 5,
        'S 4': 0,
        'S34': 6,
    }
    # layer matrix for "xmodmap" with enabled Caps Lock
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        2 |       0 |
    # | Mod3 on   |        5 |       6 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        2 |       0 |
    # | Mod3 on   |        5 |       6 |
    # |-----------+----------+---------|
    layers['xmodmap', 'caps_lock'] = {
        '   ': 2,
        ' 3 ': 5,
        '  4': 0,
        ' 34': 6,
        'S  ': 2,
        'S3 ': 5,
        'S 4': 0,
        'S34': 6,
    }
    # layer matrix for "xmodmap" with enabled Mod4 Lock
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        4 |       4 |
    # | Mod3 on   |        3 |       6 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        0 |       0 |
    # | Mod3 on   |        5 |       6 |
    # |-----------+----------+---------|
    layers['xmodmap', 'mod4_lock'] = {
        '   ': 4,
        ' 3 ': 3,
        '  4': 4,
        ' 34': 6,
        'S  ': 0,
        'S3 ': 5,
        'S 4': 0,
        'S34': 6,
    }
    # layer matrix for "xmodmap" with enabled Caps+Mod4 Lock
    #
    # |-----------+----------+---------|
    # | Shift off | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        0 |       0 |
    # | Mod3 on   |        5 |       5 |
    # |-----------+----------+---------|
    # | Shift on  | Mod4 off | Mod4 on |
    # |-----------+----------+---------|
    # | Mod3 off  |        0 |       0 |
    # | Mod3 on   |        5 |       5 |
    # |-----------+----------+---------|
    layers['xmodmap', 'caps_mod4_lock'] = {
        '   ': 0,
        ' 3 ': 5,
        '  4': 0,
        ' 34': 5,
        'S  ': 0,
        'S3 ': 5,
        'S 4': 0,
        'S34': 5,
    }


    def __init__(self):
        self.__move_window_handler = None

        # setting: display main keyboard (Boolean)
        self.display_main_keyboard = (settings.get(
            'settings', 'display_main_keyboard', True) == 'True')

        # setting: display numeric keyboard (Boolean)
        self.display_numeric_keyboard = (settings.get(
            'settings', 'display_numeric_keyboard', True) == 'True')

        self.keyboard_type = settings.get(
            'settings', 'keyboard_type', 'pc105')

        # setting: magnification of keyboard (in percent)
        self.magnification = int(settings.get(
            'settings', 'magnification_in_percent', 100))

        # setting: interval of update timer (in milliseconds)
        self.polling = int(settings.get(
            'settings', 'polling_in_milliseconds', DEFAULT_POLLING_INTERVAL))

        self.appear_on_all_desktops = (settings.get(
            'settings', 'appear_on_all_desktops', True) == 'True')

        # setting: selected driver ("xkbdmap" or "xmodmap")
        self.keyboard_driver = settings.get(
            'settings', 'selected_keyboard_driver', 'xkbdmap')

        # setting: last iconification status
        self.iconified = (settings.get(
            'settings', 'iconified', True) == 'True')

        self.status_icon = statusicon.StatusIcon(
            self,
            os.path.join(package_path, 'images', 'neo-icon.svg'),
            visible=False)

        # initialise core keyboard
        self.initialise_keyboard()

        # set currently selected keyboard layer to "unset"
        self.current_modifier = None
        self.mod_states = None

        # create main window and set its title
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title(settings.get_description(False))

        # Tell the window manager to no activate the window and to no
        # add it to the doc, ...
        self.window.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        # ... and have it on all desktops (if requested)
        if self.appear_on_all_desktops:
            self.window.stick()

        # set up for moving the window
        self.window.set_decorated(False)
        self.window.connect('button_press_event', self.on_button_press)

        # allow window to get killed and keep it on top
        self.window.connect('delete-event', self.on_delete_event)
        self.window.set_keep_above(True)

        # restore old window position
        x = int(settings.get('settings', 'window_position_x', 0))
        y = int(settings.get('settings', 'window_position_y', 0))
        self.window.move(x, y)

        self.window.connect('button_release_event', self.on_button_release)

        # create an HBox, ...
        self.hbox = Gtk.HBox(False, DISTANCE_LAYOUT_BLOCKS)
        self.window.add(self.hbox)

        # ..., attach images for main and numeric keyboards
        self.image_main = Gtk.Image()
        self.hbox.pack_start(self.image_main, True, True, 0)
        self.image_numeric = Gtk.Image()
        self.hbox.pack_start(self.image_numeric, True, True, 0)

        # update status of modifier keys and display once ...
        # Later on, the keyboard layout will only be drawn when the
        # selected keyboard layer changes, so we'll force the initial
        # drawing
        self.update_status()

        if self.keyboard_driver == 'xkbdmap':
            self._xmodmap_timer = None
            # If we have XKB, we use an event listener
            GObject.threads_init()
            self._xkb_event_listener = xkb_event_listener.EventListener(self)
            self._xkb_event_listener.start()
        else:
            # Otherwise we need to start a timer for polling modifier keys
            self._xkb_event_listener = None
            self._xmodmap_timer = GObject.timeout_add(
                self.polling, self.update_status)

        if self.iconified:
            self.do_iconify()
        else:
            # show everything in window
            self.window.show_all()


    def on_button_press(self, widget, event):
        if event.button == 1:
            if event.type == Gdk.EventType._2BUTTON_PRESS:
                self.do_iconify()
                self._end_window_move(event)
            else:
                self._start_window_move(event)
            return True
        elif event.button == 3:
            self._pop_settings_menu(event)
            return True


    def on_button_release(self, widget, event):
        if event.button == 1:
            self._end_window_move(event)
            return True

    def _pop_settings_menu(self, event):
        menu = self._create_menu()
        menu.popup(None, None, None, None, event.button, event.get_time())

    def _start_window_move(self, event):
        if self.__move_window_handler:
            return
        x, y = self.window.get_position()
        self.__move_window_start = (event.x_root-x, event.y_root-y)
        hid = self.window.connect('motion_notify_event', self._on_move_window)
        self.__move_window_handler = hid

    def _end_window_move(self, event):
        if self.__move_window_handler:
            self.window.disconnect(self.__move_window_handler)
            self.__move_window_handler = None
            self._on_move_window(None, event)

    def _on_move_window(self, widget, event):
        x, y = self.__move_window_start
        x, y = (event.x_root-x, event.y_root-y)
        self.window.move(int(x), int(y))


    def _create_menu(self):
        menu = Gtk.Menu()
        for name, varname in (
                (_("Display _Main Keyboard"), 'display_main_keyboard'),
                (_("Display _Numeric Keyboard"), 'display_numeric_keyboard'),
                (_("on all Desktops"), 'appear_on_all_desktops'),
                ):
            item = Gtk.CheckMenuItem(name, use_underline=True)
            item.connect("toggled", self.on_bool_settings_response, varname)
            item.set_active(getattr(self, varname))
            menu.append(item)

        menu.append(Gtk.SeparatorMenuItem())
        item = Gtk.MenuItem(_("Settings …"), use_underline=True)
        item.connect("activate", self.on_open_settings_dialog)
        menu.append(item)

        menu.append(Gtk.SeparatorMenuItem())

        exit = Gtk.MenuItem(_("Quit"), use_underline=True)
        exit.connect("activate", self.on_delete_event)
        menu.append(exit)

        menu.show_all()
        return menu


    def on_bool_settings_response(self, widget, varname):
        is_active = widget.get_active()
        setattr(self, varname, is_active)
        settings.set('settings', varname, is_active)
        if varname == 'appear_on_all_desktops':
            if self.appear_on_all_desktops:
                self.window.stick()
            else:
                self.window.unstick()
        else:
            self.update_display()
        return True

    def on_open_settings_dialog(self, widget):
        import osd_neo2.settings_dialog
        base = osd_neo2.settings_dialog.SettingsDialog(self, None)
        return True


    def main(self):
        # main event loop
        try:
            Gtk.main()
        except KeyboardInterrupt:
            # stop the xkb listener (if used)
            if self._xkb_event_listener:
                self._xkb_event_listener.stop()


    def on_delete_event(self, widget, event=None, data=None):
        self.do_quit()
        return True


    def do_iconify(self):
        self.status_icon.show()
        self.window.hide()
        self.iconified = True
        if self._xkb_event_listener:
            self._xkb_event_listener.stop_listen()
        else:
            GObject.source_remove(self._xmodmap_timer)
            self._xmodmap_timer = None
        return True


    def do_deiconify(self):
        self.window.show_all()  # use show_all here since the app may
        # have started iconified and `show_all()` was not yet called.
        # :todo: find a more "correct way" to start iconified.
        self.status_icon.hide()
        self.iconified = False
        if self._xkb_event_listener:
            self._xkb_event_listener.start_listen()
        else:
            assert self._xmodmap_timer is None
            self._xmodmap_timer = GObject.timeout_add(
                self.polling, self.update_status)
        return True


    def do_quit(self):
        # stop the xkb listener (if used)
        if self._xkb_event_listener:
            self._xkb_event_listener.stop()
        # store current window position, ...
        (x,y) = self.window.get_position()
        settings.set('settings', 'window_position_x', x)
        settings.set('settings', 'window_position_y', y)
        # ... and iconify state ...
        settings.set('settings', 'iconified', self.iconified)

        # ... and quit the application
        Gtk.main_quit()
        return False


    def initialise_keyboard(self):
        # initialise wrapper for the X Keyboard Extension (v1.0) and
        # open connection to X display

        # we'll use the default X display
        display_name = None

        # we need version 1.0 of the X Keyboard Extension
        major_in_out = 1
        minor_in_out = 0

        # open X display and check for compatible X Keyboard Extension
        try:
            ret = xkb.XkbOpenDisplay(display_name, major_in_out,
                                     minor_in_out)
        except OSError as error:
            self.error_dialog(_('Error'), error)

        # store handle to X display for later use
        self.display_handle = ret['display_handle']


    def update_status(self):
        """
        This function is called by the timer in order to check the
        status of modifier keys.
        """

        # we only have to update the main window if the modifier
        # states have changed, so store the current modifier states
        old_mod_states = self.mod_states

        # select the core keyboard ...
        device_spec = xkb.XkbUseCoreKbd

        # ... and poll modifier state
        xkbstaterec = xkb.XkbGetState(self.display_handle, device_spec)
        self.mod_states = xkb.ExtractLocks(xkbstaterec)

        # as promised above, we'll only update the main window if the
        # modifier states have changed
        if self.mod_states != old_mod_states:
            self.set_current_modifier()

        # keep the timer running
        return True


    def set_current_modifier(self):
        # we'll keep CPU usage low by updating the main window only
        # when the selected keyboard layer has changed, so let's store
        # the currently selected keyboard layer
        old_modifier = self.current_modifier

        # please don't confuse the modifiers defined by Neo2 ("MOD3"
        # in the following section) with modifiers defined by X11
        # ("mod3") -- let's set the modifiers for accessing the layer
        # matrices

        if self.keyboard_driver == 'xkbdmap':
            # user selected Neo2 keyboard driver "xkbdmap"
            SHIFT = 'S' if self.mod_states['shift'] else ' '
            MOD3  = '3' if self.mod_states['mod5'] else ' '
            MOD4  = '4' if self.mod_states['mod3'] else ' '
            # get status of locks
            CAPS_LOCK = self.mod_states['lock_lock']
            MOD4_LOCK = self.mod_states['mod2_lock']
        elif self.keyboard_driver == 'xmodmap':
            # user selected Neo2 keyboard driver "xmodmap"
            SHIFT = 'S' if self.mod_states['shift'] else ' '
            MOD4  = '4' if self.mod_states['mod3'] else ' '
            if self.mod_states['group'] == 0:
                MOD3 = ' '
            elif self.mod_states['group'] == 1:
                MOD3 = '3'
            elif self.mod_states['group'] == 2:
                MOD3 = '3'
                MOD4 = '4'
            # get status of locks
            CAPS_LOCK = self.mod_states['shift_lock']
            MOD4_LOCK = self.mod_states['mod3_lock']
        else:
            # user selected invalid Neo2 keyboard driver
            error = (_('Invalid keyboard driver "%s" selected.') %
                     self.keyboard_driver)
            self.error_dialog(_('Error'), error)

        # assemble matrix key
        MODIFIERS = ''.join((SHIFT, MOD3, MOD4))

        # select correct matrix and get current layer for Neo2
        layertype = {
            (False, False): 'plain',
            (False, True ): 'caps_lock',
            (True,  False): 'mod4_lock',
            (True,  True ): 'caps_mod4_lock',
            }[CAPS_LOCK, MOD4_LOCK]
        current_modifier = self.layers[self.keyboard_driver, layertype][MODIFIERS]

        # for your information, "Ebene" is German for "layer", while
        # "leer" is German for "empty"
        if current_modifier < 1:
            self.current_modifier = 'leer'
        elif current_modifier > 6:
            # add Caps Lock to layers 1 and 2
            self.current_modifier = 'ebene%d-caps' % (current_modifier - 6)
        else:
            # plain (i.e. no locks)
            self.current_modifier = 'ebene%d' % current_modifier

        # as promised above, we'll only update the main window if the
        # selected keyboard layer has changed
        if self.current_modifier != old_modifier:
            self.update_display()


    def update_display(self):
        # Displaying none of the both does not make much sense. In
        # this case simply show both.
        if not (self.display_main_keyboard or self.display_numeric_keyboard):
            self.display_main_keyboard = True
            self.display_numeric_keyboard = True

        window_width = 0
        window_height = 0

        if not self.display_main_keyboard:
            self.image_main.hide()
        else:
            current_modifier = self.current_modifier
            basename = 'neo2-hauptfeld_'
            if self.keyboard_type == 'ergodox':
                basename = 'ergodox-'
                if current_modifier != 'leer':
                    # strip '-caps' if any
                    current_modifier = current_modifier[5]
                    # same image for layer 1 and two
                    if current_modifier in '12':
                        current_modifier = '12'
            # check whether image for main keyboard exists
            path_main = os.path.join(package_path, 'images',
                                     basename + current_modifier + '.png')
            if not os.path.exists(path_main):
                error = (_('The following image file was not found:\n"%s"') %
                         path_main)
                self.error_dialog(_('Error'), error)

            # load image for main keyboard in PixBuf, ...
            pixbuf_main = GdkPixbuf.Pixbuf.new_from_file(path_main)

            # ... re-size it according to "self.magnification" ...
            if self.magnification != 100:
                pixbuf_main = pixbuf_main.scale_simple(
                    int(pixbuf_main.get_width() * self.magnification / 100),
                    int(pixbuf_main.get_height() * self.magnification / 100),
                    GdkPixbuf.InterpType.BILINEAR)
            # ... and copy it to the main window
            self.image_main.set_from_pixbuf(pixbuf_main)
            self.image_main.show()
            window_width = pixbuf_main.get_width()
            window_height = pixbuf_main.get_height()

        if not self.display_numeric_keyboard:
            self.image_numeric.hide()
        else:
            # check whether image for numeric keyboard exists
            path_numeric = os.path.join(package_path, 'images',
                                            'neo2-ziffernfeld_' + \
                                            self.current_modifier + '.png')
            if not os.path.exists(path_numeric):
                error = (_('The following image file was not found:\n"%s"') %
                         path_numeric)
                self.error_dialog(_('Error'), error)

            # load image for numeric keyboard in PixBuf, ...
            pixbuf_numeric = GdkPixbuf.Pixbuf.new_from_file(path_numeric)
            # ... re-size it according to "self.magnification" ...
            if self.magnification != 100:
                pixbuf_numeric = pixbuf_numeric.scale_simple(
                    int(pixbuf_numeric.get_width() * self.magnification / 100),
                    int(pixbuf_numeric.get_height() * self.magnification / 100),
                    GdkPixbuf.InterpType.BILINEAR)
            # ... and copy it to the main window
            self.image_numeric.set_from_pixbuf(pixbuf_numeric)

            window_width += pixbuf_numeric.get_width()
            if self.display_main_keyboard:
                window_width += DISTANCE_LAYOUT_BLOCKS
            window_height = max(window_height, pixbuf_numeric.get_height())
            self.image_numeric.show()

        # re-size main window accordingly
        self.window.resize(window_width, window_height)
        self.window.set_size_request(window_width, window_height)


    def error_dialog(self, title, error):
        # display a dialog with the given error ...
        dialog = Gtk.Dialog(title, None, Gtk.DialogFlags.NO_SEPARATOR,
                            (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        dialog.vbox.pack_start(Gtk.Label(str(error, True, True, 0)))
        dialog.show_all()
        dialog.run()
        # ... and exit after user has pressed "Ok"
        exit(1)
