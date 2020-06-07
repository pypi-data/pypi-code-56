#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Useful stuffs."""

import logging
import os
import os.path
import re
import subprocess
import sys

from prettyetc.etccore import confmgr
from prettyetc.etccore.langlib import RootField
from prettyetc.etccore.langlib.parsers import BadInput
from prettyetc.etccore.logger import LoggerCreator, errhelper

__all__ = ("get_desktop_environment", "open_callback", "create_configfactory",
           "init_logger", "read_autoselect")


def get_desktop_environment() -> str:  # pylint: disable=R0911,R0912
    """
    Get the current DE on linux.

    From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    and http://ubuntuforums.org/showthread.php?t=652320
    and http://ubuntuforums.org/showthread.php?t=652320
    and http://ubuntuforums.org/showthread.php?t=1139057
    """

    if sys.platform in ["win32", "cygwin"]:
        return "windows"
    if sys.platform == "darwin":
        return "mac"
    # Most likely either a POSIX system or something not much common
    desktop_session = os.environ.get("DESKTOP_SESSION")
    if desktop_session is not None:  #easier to match if we doesn't have  to deal with caracter cases
        desktop_session = desktop_session.lower()
        if desktop_session in ("gnome", "unity", "cinnamon", "mate", "xfce4",
                               "lxde", "fluxbox", "blackbox", "openbox",
                               "icewm", "jwm", "afterstep", "trinity", "kde"):
            return desktop_session
        ## Special cases ##
        # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
        # There is no guarantee that they will not do the same with the other desktop environments.
        if "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
            return "xfce4"
        if desktop_session.startswith("ubuntu"):
            return "unity"
        if desktop_session.startswith("lubuntu"):
            return "lxde"
        if desktop_session.startswith("kubuntu"):
            return "kde"
        if desktop_session.startswith("razor"):  # e.g. razorkwin
            return "razor-qt"
        if desktop_session.startswith("wmaker"):  # e.g. wmaker-common
            return "windowmaker"
    if os.environ.get('KDE_FULL_SESSION') == 'true':
        return "kde"
    if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
        if not "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            return "gnome2"
    #From http://ubuntuforums.org/showthread.php?t=652320
    if is_running("xfce-mcs-manage"):
        return "xfce4"
    if is_running("ksmserver"):
        return "kde"
    return "unknown"


def is_running(process) -> bool:
    """
    Check if given process is running.

    From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
    and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
    """

    try:  # Linux/Unix
        results = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    except OSError:  # Windows
        results = subprocess.Popen(["tasklist", "/v"], stdout=subprocess.PIPE)
    for res in results.stdout:
        if re.search(process, res):
            return True
    return False


def open_callback(ui, path, configfactory, *_):
    """
    Add root field to ui by processing the given config.

    .. versionchanged:: 0.3.0
        This function no longer works with new :class:`~prettyetc.baseui.ui.main.BaseMain`.

    .. deprecated:: 0.2.0
        This function is being moved to :class:`~prettyetc.baseui.main.BaseMainUi`.


    """
    configfile = configfactory(path)
    root = configfile.read(configfactory.matcher)
    if isinstance(root, BadInput):
        ui.handle_badinput(path, root)
    elif isinstance(root, RootField):
        ui.add_root(root)
    else:
        raise errhelper(TypeError("Bad root returned"), ui.logger)


def create_configfactory(*plugin_paths: str, plugin_files: iter = None
                        ) -> confmgr.ConfigFileFactory:
    """Create and configure a ConfigFileFactory object."""
    if plugin_paths and hasattr(plugin_paths[0], "__iter__"):
        plugin_paths = plugin_paths[0]
    factory = confmgr.ConfigFileFactory(
        *plugin_paths, plugin_files=plugin_files)
    return factory


def init_logger(loggername="prettyetc",
                log_level: int = logging.WARNING,
                logfile: str = "prettyetc.log",
                **kwargs) -> LoggerCreator:
    """Init logger."""
    rootlogger = logging.getLogger(loggername)
    rootlogger = LoggerCreator(
        rootlogger, log_level=log_level, logfile=logfile, **kwargs)
    return rootlogger


def read_autoselect(result,
                    rootfield: callable = lambda *args: None,
                    badinput: callable = lambda *args: None):
    """
    Select the properly callback based on result type.
    Callbacks receive the given result as its first (required) parameter.

    At the moment only :class:`~prettyetc.etccore.langlib.root.RootField` and
    :class:`~prettyetc.etccore.langlib.parsers.BadInput` objects are supported.

    :raises TypeError: If result has an unsupported type.

    .. versionadded:: 0.3.0
    """

    if isinstance(result, BadInput):
        badinput(result)
    elif isinstance(result, RootField):
        rootfield(result)
    else:
        raise TypeError("Bad root returned")
