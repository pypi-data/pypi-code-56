#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides a convenient way to manage a
:class:`~prettyetc.baseui.settings.SettingsManager` object.

It manages the settings file path and create a stream for
:class:`~prettyetc.baseui.settings.SettingsManager` and,
if available, uses the homebase library to get the platform-dependent path for settings.

By default there is a set of settings that the
:class:`~BaseSettings` uses for its stuffs.

.. versionadded:: 0.3.0
"""
import prettyetc.etccore as etccore

from .. import settings
from .common import CommonComponent

__all__ = ("BaseSettings",)

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
        Class renamed to BaseSettings and moved to :mod:`.ui.settings`
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
            Use :meth:`.SettingsManager.init_default` method instead.
        """

    def load(self, seek: int = 0):
        """
        Load settings from :class:`~prettyetc.baseui.settings.SettingsManager`

        .. versionadded:: 0.3.0
        """
        self.settings.load(seek=seek)

    def init_ui(self, seek: int = 0):
        """Load and init configs."""
        self.load(seek=seek)
        super().init_ui()
        if type(self).init_config != BaseSettings.init_config:
            self.logger.warning(
                "The init_config method of BaseSettings is deprecated")
            self.init_config()
        self.data.init_default(DEFAULT_DATA)

    def save(self, seek: int = 0):
        """Call setting manager save as long as all required data is setted."""
        self.settings.etccore.setdefault("version", etccore.__version__)

        # end fields checks
        self.settings.save(seek=seek)

    def close(self, seek: int = 0):
        """Save the settings and close it."""
        self.save(seek=seek)
        super().close()

    def reset(self, default: dict = None):
        """
        Reset the data with given default, if available.

        :param dict default: The data to be setted after reset.

        .. .. tip::
        ..    If you want to override this method and you use :class:`super`,
        ..    don't call :meth:`.SettingsManager.reset` method direcly.

        .. versionadded:: 0.3.0
        """
        if default is None:
            default = {}
        default.update(DEFAULT_DATA)
        self.settings.reset(default)

    @property
    def data(self):
        """Settings data. This is a shorthand for :attr:`BaseSettings.settings`."""
        return self.settings
