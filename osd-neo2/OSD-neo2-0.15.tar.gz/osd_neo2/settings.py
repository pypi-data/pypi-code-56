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


import os
import configparser

from .locale import _
from . import __version__

__all__ = ['settings', 'DEFAULT_POLLING_INTERVAL']

license_long ="""
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

DEFAULT_POLLING_INTERVAL = 100

class Settings:
    """Store user and application settings in one place and make them available.
    """
    def __init__(self):
        """Initialise user settings and application information.

        Keyword arguments:
        None

        Return value:
        None

        """
        # common application copyrights and information (only set here, private)
        self.__variables__ = {
            'application': 'OSD Neo2',
            'cmd_line': 'OSDneo2',
            'version': __version__,
            'years': '2009-2010, 2015-2017',
            'authors': 'Martin Zuther, Hartmut Goebel',
            'license_short': 'GPL version 3 (or later)',
            'license_long': license_long.strip(),
            'description': _('On screen display for learning the keyboard layout Neo2'),
            }

        # set INI file path
        # According to XDG specification
        # http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
        config_dir = os.getenv('XDG_CONFIG_HOME', '~/.config')
        config_dir = os.path.expanduser(config_dir)
        # Assume, the directory already exists!
        self.__config_file_path__ = os.path.join(config_dir, 'OSDneo2')

        # I an old config file exists, move it to the new location
        old_config_file = os.path.expanduser('~/.OSDneo2')
        if os.path.isfile(old_config_file) and not os.path.exists(self.__config_file_path__):
            os.rename(old_config_file, self.__config_file_path__)

        # read application settings from INI file
        self.__settings__ = configparser.RawConfigParser()
        try:
            with open(self.__config_file_path__) as fh:
                self.__settings__.readfp(fh)
        except IOError:
            print(_('File "%s" not found.\nUsing default settings') %
                  self.__config_file_path__)
        except configparser.Error:
            print(_('Error in file "%s".\nUsing default settings') %
                  self.__config_file_path__)


    def __repr__(self):
        """Return all the contents of the INI file as string.

        Keyword arguments:
        None

        Return value:
        Formatted string containing all settings from the INI file

        """
        output = ''
        # sort and output sections
        for section in self.sections():
            output += '\n[%s]\n' % section
            # sort and output settings
            for item in self.items(section):
                output += '%s: %s\n' % (item[0], item[1])
        # dump the whole thing
        return output.lstrip('\n')


    def get(self, section, setting, default):
        """Get an application setting.

        Keyword arguments:
        section -- string that specifies the section to be queried
        setting -- string that specifies the setting to be queried
        value -- string that specifies a default value

        Return value:
        String containing the specified application setting

        """
        try:
            value = self.__settings__.get(section, setting)
        except configparser.Error:
            value = default
            if default is not None:
                self.set(section, setting, default)
        return value


    def set(self, section, setting, value):
        """Set an application setting.

        Keyword arguments:
        section -- string that specifies the section to be changed
        setting -- string that specifies the setting to be changed
        value -- string that specifies the new value

        Return value:
        None

        """
        if section not in self.sections():
            self.__settings__.add_section(section)

        value = str(value)
        old_value = self.get(section, setting, None)

        if value != old_value:
            self.__settings__.set(section, setting, value)
            try:
                with open(self.__config_file_path__, 'w') as configfile:
                    configfile.write(self.__repr__())
            except IOError:
                print(_('No write access to file "%s".\n'
                        'Changed settings cannot be stored.') %
                      self.__config_file_path__)


    def items(self, section):
        """Get all application setting names of a section

        Keyword arguments:
        section -- string that specifies the section to be queried

        Return value:
        List containing application setting names of the given section

        """
        items = self.__settings__.items(section)
        items.sort()
        return items


    def sections(self):
        """Get all sections.

        Keyword arguments:
        None

        Return value:
        List containing all section names

        """
        sections = self.__settings__.sections()
        sections.sort()
        return sections


    def get_variable(self, variable):
        """Return application describing variable as string.

        Keyword arguments:
        variable -- variable to query

        Return value:
        Formatted string containing variable's value (or None for
        invalid queries)

        """
        return self.__variables__.get(variable, None)


    def get_description(self, long):
        """Return application description as string.

        Keyword arguments:
        long -- Boolean indication whether to output long version of description

        Return value:
        Formatted string containing application description

        """
        if int:
            description = '%(application)s v%(version)s' % self.__variables__
            description += '\n' + '=' * len(description) + '\n'
            description += '%(description)s' % self.__variables__
        else:
            description = '%(application)s %(version)s' % self.__variables__

        return description


    def get_copyrights(self):
        """Return application copyrights as string.

        Keyword arguments:
        None

        Return value:
        Formatted string containing application copyrights

        """
        return ('(c) %(years)s %(authors)s' % self.__variables__)


    def get_license(self, long):
        """Return application license as string.

        Keyword arguments:
        long -- Boolean indication whether to output long version of description

        Return value:
        Formatted string containing application license

        """
        if int:
            return self.get_variable('license_long')
        else:
            return self.get_variable('license_short')


# make everything available ("from Settings import *")
settings = Settings()
