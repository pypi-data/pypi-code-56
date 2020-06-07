#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manage core and UI settings.

This module provides an UI-indipendent config manager that save settings
to a properly configuration file in the right place
(platform-dependent config folder).
"""

import io
import json
import os

from prettyetc.etccore.logger import ChildLoggerHelper, errhelper

try:
    # 3.5+ attribute
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

try:
    import homebase
except ImportError:
    homebase = None

__all__ = ("SettingsManager",)

_manager_cache = {}


class SettingsManager(ChildLoggerHelper):
    """
    Manage the UI's config file.

    It reads and writes data to a given stream.
    Only one stream is supported at the moment.

    This class can cache the settings manager objects.

    .. note::
        At the moment settings can only be saved in a json file,
        managed by standard json library.

    .. versionchanged:: 0.3.0
        Added support for the [] operator.
    """

    __slots__ = ("__data", "__stream", "__is_init")
    loggername = "baseui.settings.manager"
    logger = None

    @classmethod
    def factory(cls, input, homebase_use_default: bool = False):  # pylint: disable=W0622
        """
        Create a :class:`~SettingsManager` object that process the given input to a stream.

        :param input: The input object used to create the :class:`~SettingsManager` object
                      The kind of input depends of the input:

                      - if it's None, the homebase library is used for create path
                      - if it's a path, try to open the stream by the given file
                      - if it's a stream, nothing is done to the stream

        :type input: None or str or open

        :param bool homebase_use_default: Allow the use of "default" as input instead of None

            .. deprecated:: 0.3.0
                This parameter is used for backward compatibility.

        .. versionadded:: 0.3.0

        """
        if input is None or (homebase_use_default and input == "default"):
            if homebase is None:
                raise ImportError("Homebase library is not installed.")
            confdir = homebase.user_config_dir(
                "prettyetc", "trollodel", create=True)
            confpath = os.path.join(confdir, "prettyetc.conf")
            if os.path.isfile(confpath):
                confstream = open(confpath, "r+")
            else:
                confstream = open(confpath, "w+")
                confstream.write("{}")
                confstream.seek(0)

        elif isinstance(input, str):
            if os.path.isfile(input):
                confstream = open(input, "r+")
            else:
                confstream = open(input, "w+")
                confstream.write("{}")
                confstream.seek(0)

        elif isinstance(input, io.IOBase):
            confstream = input

        else:
            raise TypeError("Unsupported input typed {}".format(
                type(input).__name__))

        return cls(confstream)

    def __new__(cls, stream: open):
        """
        Cache settings objects by stream name.

        .. versionadded:: 0.3.0
        """
        name = getattr(stream, "name", None)
        if name in _manager_cache:
            obj = _manager_cache[name]
            obj.logger.debug("using cached settings for file %s", name)
            obj.__stream = stream  # pylint: disable=W0212

        else:
            obj = super().__new__(cls)

            if name is not None:
                # obj.logger.debug("settings for file %s cached", name)
                _manager_cache[name] = obj
        return obj

    def __init__(self, stream: open):
        try:
            is_init = self.__getattribute__("_SettingsManager__is_init")
        except AttributeError:
            is_init = False

        super().__init__()
        if not is_init:
            self.__data = {}
            if isinstance(
                    stream,
                    io.IOBase) and stream.readable() and stream.writable():
                self.__stream = stream
            else:
                raise TypeError(
                    "Given stream to {} is not a file-like object readable and writable.".
                    format(type(self).__name__))
            self.__is_init = True

    def __repr__(self):
        """Print data."""
        return "<SettingsManager {}>".format(
            self.__data if self else "not initialized",)

    def __getitem__(self, key):
        """
        Get item from settings data.

        .. versionadded:: 0.3.0
        """
        self.__data.__getitem__(key)

    def __setitem__(self, key, val):
        """
        Set item to settings data, the given key must be a string.

        .. versionadded:: 0.3.0
        """
        if not isinstance(key, str):
            raise TypeError("Only string keys are supported for settings.")
        self.__data.__setitem__(key, val)

    def __delitem__(self, key):
        """
        Get item from settings data.

        .. versionadded:: 0.3.0
        """
        self.__data.__delitem__(key)

    def __getattr__(self, key):
        """Implement attribute access to internal data."""
        if self.__getattribute__("_SettingsManager__data") is None:
            raise ValueError("Data is not initialized")
        try:
            return self.__data[key]
        except KeyError:
            raise AttributeError(
                "'{}' object has not attribute '{}' initialized.".format(
                    type(self).__name__,
                    key,
                ))

    def __setattr__(self, key, value):
        if key in ("_SettingsManager__data", "_SettingsManager__stream",
                   "_SettingsManager__is_init", "logger"):
            super().__setattr__(key, value)
        else:
            self.__data[key] = value

    def __delattr__(self, key):
        if key in ("__data", "__stream"):
            super().__delattr__(key)
        else:
            del self.__data[key]

    def __bool__(self) -> bool:
        """Return bool(data)."""
        return bool(self.__data)

    # stream manipulation
    def load(self, seek=0, update: bool = False):
        """Read the file from the given position.
        If update if True, data will not being replaced, but updated."""
        self.__stream.seek(seek)
        try:
            if update:
                self.__data.update(json.load(self.__stream))
            else:
                self.__data = json.load(self.__stream)
        except (JSONDecodeError, UnicodeDecodeError) as ex:
            self.logger.warning(
                "Ignoring a %s error occurred when settings file is readed, "
                "set data to an empty dict.",
                type(ex).__name__)
            if not self:
                self.__data = {}

    def save(self, seek=0):
        """Write the file from the given position."""
        self.logger.debug("Save settings to stream.")
        self.__stream.seek(seek)
        self.__stream.truncate()
        json.dump(self.__data, self.__stream)
        # self.__stream.flush()

    # data manipulation
    def init_default(self, default_tree: dict):
        """
        Set default value to settings.

        .. versionadded:: 0.3.0
        """

        def _recursive_default(tree: dict, data: dict):
            for key, val in tree.items():
                if isinstance(val, dict):
                    data.setdefault(key, {})
                    _recursive_default(val, data[key])

                else:
                    data.setdefault(key, val)

        _recursive_default(default_tree, self.__data)

    def reset(self, default: dict = None):
        """
        Erase all data.

        :param dict default: Default data setted after erasing.
                             By default is None that let
                             :class:`~SettingsManager` to choose.

        .. versionadded:: 0.3.0

        """
        if default is None:
            self.__data = {}
        elif isinstance(default, dict):
            self.__data = default
        else:
            raise errhelper(
                TypeError("Default data must be a dict, got {}".format(
                    type(self).__name__)),
                self.logger,
            )

    # getters
    def stream(self):
        """
        Get internal steam.

        .. versionadded:: 0.3.0
        """
        return self.__stream

    # extra utils
    def move(self, newpath, removeold=True):
        """
        Move old configuration file to new path.

        It reads all the old stream content (seeking the begin)
        and write it to new path.

        .. warning::
            This method doesn't save data before moving.
        """
        stream = open(newpath, "w+")
        self.__stream.seek(0)
        stream.write(self.__stream.read())
        if removeold:
            os.remove(self.__stream.name)
        self.__stream.close()
        self.__stream = stream
