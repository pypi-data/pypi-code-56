#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========
Settings UI
===========

This module provides a convenient way to manage a
:class:`~prettyetc.baseui.settings.SettingsManager` object.

It manages the settings file path and create a stream for
:class:`~prettyetc.baseui.settings.SettingsManager` and,
if avaiable, uses the homebase library to get the platform-dependent path for settings.

By default there is a set of settings that the
:class:`~BaseSettings` uses for its stuffs.


.. versionadded:: 0.3.0
"""
import prettyetc.etccore as etccore
from prettyetc.baseui import settings

from .common import CommonComponent

__all__ = ("BaseSettings", )

DEFAULT_DATA = {"etccore": {}}


class BaseSettings(CommonComponent):  # pylint: disable=W0223
    """
    Represents the setting instance of an ui.

    It defines a set of abstract methods that provide an interface to settings manager.
    Also it defines a minimum set of configurations.

    Basic configurations:
        - etccore:
            - core version

    .. versionchanged:: 0.3.0
        Class renamed to BaseSettings and moved to :mod:`prettyetc.baseui.ui.settings`
    """
    loggername = "baseui.settings.ui"

    def __init__(self, input, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = settings.SettingsManager.factory(
            input, homebase_use_default=True)

        self.logger.info("Configuration file setted to {}".format(
            self.settings.stream().name))

    def init_config(self):
        """
        Init configs.

        .. deprecated:: 0.3.0
            Use :meth:`~prettyetc.baseui.settings.SettingsManager.init_default` method instead.
        """
        self.logger.debug(
            "The init_config method of BaseSettings is deprecated")

    def load(self, seek=0):
        """
        Load settings from :class:`~prettyetc.baseui.settings.SettingsManager`

        .. versionadded:: 0.3.0
        """
        self.settings.load(seek=seek)

    def init_ui(self, seek=0):
        """Load and init configs."""
        self.load(seek=seek)
        super().init_ui()
        self.init_config()
        self.data.init_default(DEFAULT_DATA)

    def save(self, seek=0):
        """Call setting manager save as long as all required data is setted."""
        # field checks
        # COMING SOON
        self.settings.etccore.setdefault("version", etccore.__version__)

        # end fields checks
        self.settings.save(seek=seek)

    def close(self, seek=0):
        """Save settings and close the settings."""
        self.save(seek=seek)
        super().close()

    def reset(self, default: dict = None):
        """
        Reset the data with given dict, if avaiable.

        .. tip::
            If you want to override this method and using super,
            don't call :meth:`~prettyetc.baseui.settings.SettingsManager.reset`

        .. versionadded:: 0.3.0
        """
        if default is None:
            default = {}
        default.update(DEFAULT_DATA)
        self.settings.reset(default)

    @property
    def data(self):
        """Settings data."""
        return self.settings
