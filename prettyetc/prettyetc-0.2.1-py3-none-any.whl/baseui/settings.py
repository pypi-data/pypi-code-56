#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========
Settings
========

Manage and view ui settings.
This module provides a base for the settings ui and
a ui-indipendent config manager that save settings
to a properly configuration file in the right place
(platform-dependent config folder).

This module provide 2 classes:

The py:class:`SettingsManager` provides a convenient way to load and save configuration.

The py:class:`BaseSettingsUi` provides a convenient way to manage a SettingsManager object,
making properly controls before saving.
"""

import io
import json
import os

import prettyetc.etccore as etccore
from prettyetc.etccore.logger import ChildLoggerHelper

try:
    import homebase
except ImportError:
    homebase = None

try:
    # 3.5+ attribute
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

# try:
#     import homebase
# except ImportError:
#     homebase = None

__all__ = ("SettingsManager", "BaseSettingsUi")


class SettingsManager(ChildLoggerHelper):
    """
    Manage the ui's config file.

    It read and write data to a given stream.
    Only one stream is supported at the moment.

    .. note::
        At the moment settings can only be saved in a json file,
        managed by stdlib json library.
    """

    __slots__ = ("__data", "__stream")
    loggername = "baseui.settings.manager"
    logger = None
    def __init__(self, stream):
        self.__data = {}
        super().__init__()
        if isinstance(stream,
                      io.IOBase) and stream.readable() and stream.writable():
            self.__stream = stream
        else:
            raise TypeError(
                "Given stream to {} is not a file-like object readable and writable.".
                format(type(self).__name__))

    def __repr__(self):
        """Print data."""
        return "<SettingsManager {}>".format(self.__data)

    def __getattr__(self, key):
        """Implement attribute access to internal data."""
        if self.__getattribute__("_SettingsManager__data") is None:
            raise ValueError("Data is not initialized")
        try:
            return self.__data[key]
        except KeyError:
            raise AttributeError(
                "'{}' object has not attribute '{}' initialized.".format(
                    type(self).__name__, key))

    def __setattr__(self, key, value):
        if key in ("_SettingsManager__data", "_SettingsManager__stream"):
            super().__setattr__(key, value)
        else:
            self.__data[key] = value

    def __delattr__(self, key):
        if key in ("__data", "__stream"):
            super().__delattr__(key)
        else:
            del self.__data[key]

    def __bool__(self):
        """Return bool(data)."""
        return bool(self.__data)

    def load(self, seek=0):
        """Read the file from the given position."""
        self.__stream.seek(seek)
        try:
            self.__data = json.load(self.__stream)
        except (JSONDecodeError, UnicodeDecodeError) as ex:
            self.logger.warning(
                "Ignoring a %s error occurred when settings file is readed, "
                "set data to an empty dict.",
                type(ex).__name__)
            self.__data = {}

    def save(self, seek=0):
        """Write the file from the given position."""
        self.logger.debug("Save settings to stream.")
        self.__stream.seek(seek)
        self.__stream.truncate()
        json.dump(self.__data, self.__stream)
        # self.__stream.flush()

    def move(self, newpath, removeold=True):
        """
        Move old configuration file to new path.

        It reads all the old stream content (seeking the begin)
        and write it to new path.

        .. warning::
            This- method doesn't save data before moving.
        """
        stream = open(newpath, "w+")
        self.__stream.seek(0)
        stream.write(self.__stream.read())
        if removeold:
            os.remove(self.__stream.name)
        self.__stream.close()
        self.__stream = stream


class BaseSettingsUi(ChildLoggerHelper):
    """
    Represents the setting instance of an ui.

    It defines a set of abstract methods that provide an interface to settings manager.
    Also it defines a minimum set of configurations.

    Basic configurations:
        - etccore:
            - core version
    """
    loggername = "baseui.settings.ui"

    def __init__(self, confstream, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if confstream == "default":
            if homebase is None:
                raise ImportError("Homebase library is not properly installed")
            confdir = homebase.user_config_dir(
                "prettyetc", "trollodel", create=True)
            confpath = os.path.join(confdir, "prettyetc.conf")
            self.logger.info(
                "Configuration file setted to {}".format(confpath))
            if os.path.isfile(confpath):
                confstream = open(confpath, "r+")
            else:
                confstream = open(confpath, "w+")
                confstream.write("{}")
                confstream.seek(0)

        self.settings = SettingsManager(confstream)
        self.init_config()

    def init_config(self):
        """Init configs."""
        self.settings.load()
        if not hasattr(self.settings, "etccore"):
            self.settings.etccore = {}  # pylint: disable=W0201

    def save(self, seek=0):
        """Call setting manager save as long as all required data is setted."""
        # field checks
        # COMING SOON
        if not self.settings.etccore.get("version", False):
            self.settings.etccore["version"] = etccore.__version__

        # end fields checks
        self.settings.save(seek=seek)

    @property
    def data(self):
        """Get the setting data."""
        return self.settings
