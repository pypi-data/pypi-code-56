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
based on 2 module attrubutes.

.. seealso::
    `PEP 8 - Public and Internal Interfaces <https://www.python.org/dev/peps/pep-0008/#id50>`_
    for more information about :code:`__all__`.
"""
import glob
import importlib
import importlib.util
import logging
import os
import pkgutil
import re
import site
import sys
import types

from .langlib import parsers, serializers
from .logger import ChildLoggerHelper, errhelper

try:
    import pkg_resources
except ImportError:
    pkg_resources = None

__all__ = ("PluginBase", "PluginManager")

REGEX_NON_ALPHANUMERIC = re.compile(r"\W")


class PluginBase(object):
    """
    Abstract base of every plugin classes.
    At the moment this class is empty and useless and
    it is intended to be used only for internal uses or advanced ones

    .. versionchanged:: 0.4.0
        This class no longer required to be inhitered.
    """

    # TO-DO: require docs and removing
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

    It fetches modules to find useful object
    (using the __all__ special constant) and register and save it.

    At the moment it only looks for subclasses of :class:`.BaseParser`
    and :class:`.BaseSerializer`, that are saved into
    :attr:`PluginManager.loaded_parsers` dictionary for :class:`.BaseParser` subclasses,
    and :attr:`PluginManager.loaded_serializers` dictionary
    for :class:`.BaseSerializer` subclasses.

    Any other object or class will be discarded with a warning.

    .. versionchanged:: 0.4.0
        Plugin classes no longer requires to be a :class:`~PluginBase`.

        Added :class:`.BaseSerializer` support.
    """

    loggername = "etccore.plugin.manager"

    __all__ = (
        "logger",
        "_plugin_count",
        "loaded_modules",
        "loaded_parsers",
        "loaded_serializers",
    )

    def __init__(self):
        super().__init__()
        self._plugin_count = 0
        self.loaded_parsers = {}  # all subclasses of BaseParser
        self.loaded_serializers = {}  # all subclasses of BaseSerializer
        self.loaded_modules = []

    # these 4 methods below are ordered by parameter type, from object/class to folder.
    def load_plugin(self, plugincls: type,
                    suppress_raise: bool = False) -> None:
        """
        Register a new plugin class and save it into the right dictionary by its type.

        :param type plugincls: The class to be registered.
            At the moment it should be a subclass of :class:`.BaseParser`
            or :class:`.BaseSerializer`

        :param bool suppress_raise:
            By default, this method, if any occurred, logs errors, then raises it.
            If suppress_raise is True, the errors won't be raised.

        :raise TypeError: If the given class is not a subclass of :class:`.BaseParser`
                          or :class:`.BaseSerializer`
        """

        if issubclass(plugincls, parsers.BaseParser):
            if hasattr(plugincls.LANGUAGES, "__iter__"):
                for lang in plugincls.LANGUAGES:
                    self.loaded_parsers[lang] = plugincls
            else:
                self.loaded_parsers[plugincls.LANGUAGES] = plugincls
            self.logger.info("Load plugin class: %s", plugincls.__name__)

        elif issubclass(plugincls, serializers.BaseSerializer):
            if hasattr(plugincls.LANGUAGES, "__iter__"):
                for lang in plugincls.LANGUAGES:
                    self.loaded_serializers[lang] = plugincls
            else:
                self.loaded_serializers[plugincls.LANGUAGES] = plugincls
            self.logger.info("Load plugin class: %s", plugincls.__name__)

        else:
            ex = errhelper(
                TypeError("Plugin {} doesn't provide any valid feature.".format(
                    plugincls.__name__)),
                self.logger,
            )
            if not suppress_raise:
                raise ex

    def fetch_module(self, mod: types.ModuleType) -> None:
        """
        Fetch a module for finding useful attributes.

        Given module must have __all__.
        """
        if hasattr(mod, "__all__") and hasattr(mod.__all__, "__iter__"):
            for attrname in mod.__all__:
                attr = getattr(mod, attrname, None)
                if isinstance(attr, type):
                    try:
                        self.load_plugin(attr)
                    except TypeError:
                        pass
                    else:
                        continue
                elif attr is None:
                    self.logger.debug("Attribute %s isn't exists", attrname)
                    continue

                self.logger.warning(
                    "Unsupported attribute %s typed %s on module %s",
                    attr,
                    type(attr).__name__,
                    getattr(mod, "path", '""'),
                )
        else:
            self.logger.warning(
                "Module %s has no __all__ attribute, no plugins will be loaded.",
                mod.__name__)

    def load_module(self, path: str, is_folder: bool = False) -> None:
        """
        Load a module by given path, then fetch it.

        :param str path:
        """
        self._plugin_count += 1
        if isinstance(path, str):
            _, module_file = os.path.split(path)
            modname, _ = os.path.splitext(module_file)
            modname = "plugin{}_{}".format(
                self._plugin_count,
                modname,
            )
            module_path = path
            if is_folder:
                module_path = os.path.join(module_path, "__init__.py")
            spec = importlib.util.spec_from_file_location(modname, module_path)
            try:
                mod = spec.loader.load_module()
            except Exception as ex:  # pylint: disable=W0703
                self.logger.error(
                    "Failed to load plugin %s from %s",
                    modname,
                    path,
                    exc_info=ex)
                return
            self.logger.debug(
                "Load %s from %s",
                "package" if is_folder else "module",
                path,
            )
        elif isinstance(path, types.ModuleType):
            # Workaround for search_modules
            mod = path
            path = mod.__file__
            modname = mod.__name__
        else:
            raise TypeError("Expected a str, got {}".format(path))

        self.fetch_module(mod)
        if path not in self.loaded_modules:
            self.loaded_modules.append(path)

        if self.logger.isEnabledFor(logging.DEBUG) and hasattr(
                sys, "getrefcount"):
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
        :param bool only_dirs: If true this load all folders, but not modules.
                               With this flag, the skip_controls has different meaning,
                               It tells if skips the __init__.py check.

        .. tip::
            If you don't need the advanced parameters of this method,
            please use the :meth:`PluginManager.search_modules` method instead.

        .. note::
            It doesn't look into subdirectories.
        """
        if only_dirs:
            globs = "{}{}*".format(
                glob.escape(path),
                os.path.sep,
            )
        elif skip_controls:
            globs = "{}{}*.*".format(
                glob.escape(path),
                os.path.sep,
            )
        else:
            globs = "{}{}*.py".format(
                glob.escape(path),
                os.path.sep,
            )

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
            checks = (lambda filename: filename.startswith("__"),)
            for filepath in result:
                file = os.path.basename(filepath)

                if not os.path.isfile(filepath) or (skip_controls or any(
                        check(file) for check in checks)):
                    _trash_res.append(filepath)

        for trash in _trash_res:
            result.remove(trash)

        self.logger.info(
            "Found %s %s in the directory %s.",
            len(result),
            "packages" if only_dirs else "modules",
            path,
        )
        for filepath in result:
            self.load_module(filepath, is_folder=only_dirs)

    def search_modules(self,
                       paths: list = "",
                       entry_point: str = "",
                       begin: str = "",
                       end: str = "",
                       no_pkg: bool = False) -> None:
        """
        Elastic module search engine.

        This method implements some methods for finding and loading modules.
        Here are listed:

            by paths
                Given paths.
                Found modules can be filter by module name begin and
                end. Module type (file or folder) can be filtered too.
                Remember that the found modules are in module format.
                (ex. "package.module").

            by entry_point
                This method requires setuptools.
                Given entry point name, that must be setted in the setup.py file.
                Found modules can be filter by module name start and end.
                Module type (file or folder) can be filtered too.
                Remember that the found modules are in module format.
                (ex. "package.module").

        :param list paths: A list of paths to be scanned.
            If this parameter is "site", it becomes
            a list of :mod:`site` paths.

        :param str entry_point: A setuptools entry_point.
            This parameter will be passed to :func:`pkg_resources.iter_entry_points`,
            for getting all the packages market with the entry_point.

        :param str begin: Required begin of the package name.

        :param str end: Required end of the package name.

        :param bool no_pkg: If True, discard all the packages (folders).

        .. versionadded:: 0.4.0

        .. seealso::
            `The Python import system <https://docs.python.org/3/reference/import.html>`_.

            The :mod:`site` module for site packages.

            :func:`pkgutil.iter_modules` and :func:`pkg_resources.iter_entry_points`
            (from setuptools) functions.

            Setuptools `Dynamic Discovery of Services and Plugins
            <https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins>`_
            section.
        """
        logger = self.logger.getChild("search")

        if paths is not None:
            if paths == "site":
                logger.debug("Use site paths.")
                paths = site.getsitepackages() + [site.getusersitepackages()]

            if hasattr(paths, "__iter__"):

                for finder, name, ispkg in pkgutil.iter_modules(paths):
                    if name.startswith(begin) and name.endswith(
                            end) and ispkg + no_pkg < 2:
                        try:
                            mod = finder.find_module(name).load_module(name)
                        except Exception as ex:  # pylint: disable=W0703
                            self.logger.warning(
                                "Failed to load plugin %s from %s",
                                name,
                                finder.path,
                                exc_info=ex)
                            continue
                        self.logger.debug(
                            "Load %s from %s",
                            "package" if ispkg else "module",
                            finder.path,
                        )
                        self.load_module(mod)
            else:
                raise errhelper(
                    TypeError("{} is not a valid list of paths".format(paths)),
                    logger)

        elif entry_point is not None and pkg_resources is not None:
            for entry in pkg_resources.iter_entry_points(entry_point):
                mod = entry.load()
                self.loaded_modules.append(mod)
                self.fetch_module(mod)

        elif entry_point is not None and pkg_resources is None:
            raise ImportError(
                "The pkg_resources library is not available.\n"
                "Please install it using 'pip install pkg_resources'")

        else:
            self.logger.warning("Nothing to search")

    def reload_modules(self):
        """Reload all modules in loaded_modules."""
        for path in self.loaded_modules:
            self.load_module(path)
