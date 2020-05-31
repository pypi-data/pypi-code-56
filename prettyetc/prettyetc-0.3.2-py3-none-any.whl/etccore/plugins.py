#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load your module dynamically and fetch useful objects.

This module provides a convenient way to load modules and fetch its content.
The default implementation, with prettyetc specifics,
load modules and fetch its :code:`__all__` to find subclasses of PluginBase and save it,
with a way to reload (reimport and rescan) it

By default the manager does nothing to loaded objects,
so plugin activation and deactivation events are not implemented.
In particular deactivation events is not easy to be implemented unless

In this project the plugin manager load and store all language parsers.
A subclasses of this manager is also used for dynamic select an UI
based on 2 attributes.
"""

import glob
import importlib.util
import os
import re
import sys

from .langlib import parsers
from .logger import ChildLoggerHelper, errhelper

__all__ = ("PluginBase", "PluginManager")

REGEX_NON_ALPHANUMERIC = re.compile(r"\W")


class PluginBase(object):
    """Abstract base of every plugin classes."""

    # TODO: require docs and removing
    # new cloning way will use deepcopy

    # def clone(self, cls: type):
    #     """
    #     Tranfer old attributes to new cls istance.
    #
    #     .. note::
    #         An implementation of this method should be done for each subclassing.
    #
    #     :param type cls:
    #         A subclass of this class (type(self))
    #         That class should have the same (or more) attributes.
    #     """
    #     raise NotImplementedError("Plugin clone is not supported")


class PluginManager(ChildLoggerHelper):
    """
    Get objects dynamically from python modules and packages.

    It fetches modules to find useful things
    (using the __all__ special constant) and register and save it.

    At the moment it looking for subclasses of BaseParser,
    that is saved into loaded_parsers dict.
    Any other object or class will be discarded with a warning.
    """

    loggername = "etccore.plugin.manager"

    __all__ = ("logger", "_plugin_count", "loaded_modules", "loaded_parsers")

    def __init__(self):
        super().__init__()
        self._plugin_count = 0
        self.loaded_parsers = {}  # all subclasses of BaseParser
        # self.loaded_writers = {}  # all subclasses of BaseWriter
        self.loaded_modules = []

    # this 4 methods below are in order of input type, from object/class to folder.
    def load_plugin(self, plugincls: PluginBase, suppress_raise: bool = False):
        """Register a new plugin class."""
        if issubclass(plugincls, parsers.BaseParser) and hasattr(
                plugincls, "LANGUAGES"):
            if hasattr(plugincls.LANGUAGES, "__iter__"):
                for lang in plugincls.LANGUAGES:
                    self.loaded_parsers[lang] = plugincls
            else:
                self.loaded_parsers[plugincls.LANGUAGES] = plugincls
            self.logger.info("Load plugin class: %s", plugincls.__name__)
        else:
            ex = errhelper(
                TypeError(
                    "Plugin {} doesn't provide any valid feature.".format(
                        plugincls.__name__)), self.logger)
            if not suppress_raise:
                raise ex

    def fetch_module(self, mod):
        """
        Fetch a module for finding useful attributes.

        Given module must have __all__.
        """
        if hasattr(mod, "__all__"):
            for attrname in mod.__all__:
                attr = getattr(mod, attrname, None)
                if issubclass(attr, PluginBase):
                    self.load_plugin(attr)
                elif attr is None:
                    self.logger.debug("Attribute %s isn't exists", attrname)
                else:
                    self.logger.warning(
                        "Unsupported attribute %s typed %s on module %s", attr,
                        type(attr).__name__, getattr(mod, "path", ""))
        else:
            self.logger.warning(
                "Module %s has no __all__ attribute, no plugins will be loaded.",
                mod.__name__)

    def load_module(self, path: str, is_folder=False):
        """Load a module by given path, then fetch it."""
        self._plugin_count += 1
        _, module_file = os.path.split(path)
        modname, _ = os.path.splitext(module_file)
        modname = "plugin{}_{}".format(self._plugin_count, modname)
        module_path = path
        if is_folder:
            module_path = os.path.join(module_path, "__init__.py")
        spec = importlib.util.spec_from_file_location(modname, module_path)
        try:
            mod = spec.loader.load_module()
        except Exception as ex:  # pylint: disable=W0703
            self.logger.error(
                "Failed to load plugin %s from %s", modname, path, exc_info=ex)
            return
        self.logger.debug("Load %s from %s", "package"
                          if is_folder else "module", path)
        self.fetch_module(mod)
        if path not in self.loaded_modules:
            self.loaded_modules.append(path)
        refcount = sys.getrefcount(mod)
        self.logger.debug("Remaining references to %s modules: %s", modname,
                          refcount - 3 if refcount > 3 else 0)
        if modname in sys.modules:
            del sys.modules[modname]

    def fetch_folder(self,
                     path: str,
                     skip_controls: bool = False,
                     only_dirs: bool = False):
        """
        Fetch a folder for finding plugin modules.
        By default it controls only
        file that doesn't start with _ and end with.py.

        :param bool skip_controls: If True, do no controls in selected modules.
        :param bool only_dirs: If true this load all directories, but not modules.
                               With this flag, the skip_controls has different meaning,
                               It tells if skips the __init__.py check.

        .. note::
            It doesn't look into subdirectories.
        """
        if only_dirs:
            globs = "{}{}*".format(glob.escape(path), os.path.sep)
        elif skip_controls:
            globs = "{}{}*.*".format(glob.escape(path), os.path.sep)
        else:
            globs = "{}{}*.py".format(glob.escape(path), os.path.sep)

        self.logger.debug("Selected glob: %s", globs)
        result = glob.glob(globs)
        self.logger.debug("Found files/directories: %s", result)
        _trash_res = []

        if only_dirs:
            checks = (lambda dirpath: not os.path.isfile(os.path.join(dirpath, "__init__.py")),
                      lambda dirpath: dirpath.endswith("__pycache__"))
            for dirpath in result:
                if not os.path.isdir(dirpath) or (skip_controls or any(
                        check(dirpath) for check in checks)):
                    _trash_res.append(dirpath)

        elif not skip_controls:
            checks = (lambda filename: filename.startswith("__"), )
            for filepath in result:
                file = os.path.basename(filepath)

                if not os.path.isfile(filepath) or (skip_controls or any(
                        check(file) for check in checks)):
                    _trash_res.append(filepath)

        for trash in _trash_res:
            result.remove(trash)

        self.logger.info("Found %s %s in the directory %s.", len(result),
                         "packages" if only_dirs else "modules", path)
        for filepath in result:
            self.load_module(filepath, is_folder=only_dirs)

    def reload_modules(self):
        """Reload all modules in loaded_modules."""
        for path in self.loaded_modules:
            self.load_module(path)
