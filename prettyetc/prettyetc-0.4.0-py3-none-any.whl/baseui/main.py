#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains some abstract classes for the main UI manager."""

import argparse
import inspect
import logging
import os
import sys
import traceback

from prettyetc.etccore import DEBUG2, ConfigFileFactory, PluginManager

from .cmdargs import parse_args
from .ui.main import BaseMain
from .utils import create_configfactory, init_logger

__all__ = ("BaseMainUi", "UiLauncher")
BaseMainUi = BaseMain


class UiLauncher(PluginManager):
    """
    This class scan the prettyetc directory to find launchable uis
    and provide a convenient way to launch it.

    A valid UI is a module (or a package with an __init__.py module)
    where there are at least 2 these attributes
    (inserted into the __all__ attrubute if exists):

    - __main_class__
        This class **must** be a subclass of :class:`~prettyetc.baseui.ui.main.BaseMain`
        and its signature must be the same (plus extra keyword arguments if you want)
        in order to launch the UI.
    - __prettyetc_ui__ or the attribute uiname of __main_class__
        Contains the name of the ui.
        It is used for preferring an UI (via the preferred_uis attribute).
        This name is not unique, (and should not) because the name could
        contain information about Ui library used, for example.

    These attributes are used BOTH to launch an UI.

    .. versionchanged:: 0.4.0
        Now the UI name can be found in the attribute uiname of __main_class__
    """

    loggername = "baseui.main.loader"

    def __init__(self, preferred_uis: tuple = ()):
        # do not use logging here since it is not ready
        super().__init__()
        self.preferred_uis = preferred_uis
        self.loaded_uis = []
        del self.loaded_parsers

    # PluginManager overrides
    def load_plugin(self, uiname: str, uiclass: BaseMainUi):
        """Register a new ui."""
        if (uiname, uiclass) not in self.loaded_uis:
            if issubclass(uiclass, BaseMainUi):
                self.loaded_uis.append((uiname, uiclass))
            else:
                self.logger.warning(
                    "The class %s is not an instance of BaseMainUi.",
                    getattr(uiclass, "__name__",
                            type(uiclass).__name__))

    def fetch_module(self, mod):
        """
        Fetch a module for finding useful attributes.

        Given module must have __prettyetc_ui__ and __main_class__ attributes.
        """
        uiclass = getattr(mod, "__main_class__", None)
        uiname = getattr(mod, "__prettyetc_ui__", None)
        if uiclass is None or (uiname is None and uiclass.uiname is None):
            self.logger.log(
                11, "Skipping module %s as not contains a valid UI reference.",
                mod.__name__)
        else:
            self.load_plugin(uiclass.uiname
                             if uiname is None else uiname, uiclass)

    # UIs management
    def find_uis(self, path: str = None):
        """Scan the prettyetc directory (or the given one) to find a valid ui."""
        if path is None:
            path = os.path.dirname(inspect.getfile(inspect.currentframe()))
            path = os.path.dirname(path)
        self.logger.debug("Load UIs from %s", path)
        # load both directories and modules
        self.fetch_folder(path, only_dirs=True)
        self.fetch_folder(path)

    def sort_uis(self):
        """
        Sort the UI list by preferred_uis.
        It won't do nothing if there isn't any preferred ui.
        """
        if self.preferred_uis:
            new_list = []
            for pref_ui in set(self.preferred_uis):
                for name, klass in self.loaded_uis:
                    if name == pref_ui:
                        new_list.append((name, klass))
                        self.loaded_uis.remove((name, klass))
            new_list.extend(self.loaded_uis)
            self.loaded_uis = new_list

    # ui initializing and creation
    def init_anxillary_stuffs(  # pylint: disable=W0703, R0912
            self,
            loggername: str = "prettyetc",
            log_level: int = logging.WARNING,
            logfile: str = "prettyetc.log",
            plugin_paths: iter = (),
            plugin_files: iter = None,
            namespace: argparse.Namespace = None) -> list:
        """
        Init automatically all stuffs that required to be initialized with configurations.
        It uses keyword arguments given or use an argparse.Namespace to get the parameters
        (according to the :func:`.cmdargs.create_parser` function).

        It create and manage (if necessary) all classes and objects
        that would be created before doing anything else.

        Classes and object managed
        (see classes and modules documentation for more details about these listed classes)


        - :class:`~prettyetc.etccore.logger.LoggerCreator` object
          (via :func:`.utils.init_logger`)

         The logger inizializer.
         Can be configured with:

          - logging level
          - root logger name
          - log path

        - :class:`~prettyetc.etccore.confmgr.ConfigFileFactory` object
          (via :func:`.utils.create_configfactory`)

         It inizialize the :class:`~prettyetc.etccore.confmgr.ConfigFile` object factory.
         The :class:`~prettyetc.etccore.confmgr.ConfigFileFactory`
         also inizialize the plugin manager and the file matcher,
         all of these are necessary to parse configurations files.
         Can be configured with:

          - plugin paths
          - plugin modules

        This function return all the objects created.
        The order of returned objects is the same of listed classes above.

        .. warning ::
            If one of object fail to be created,
            an exception is provided instead of the expected objects.
        """
        objects = []

        if namespace is not None:
            # Extract data from parsed arguments
            loggername = getattr(namespace, "loggername", loggername)
            if hasattr(namespace, "verbose"):
                verbosity = getattr(namespace, "verbose")
                if verbosity == 1:
                    log_level = logging.INFO
                elif verbosity == 2:
                    log_level = DEBUG2
                elif verbosity > 2:
                    log_level = logging.DEBUG
            elif getattr(namespace, "quiet", False):
                log_level = logging.ERROR
            logfile = getattr(namespace, "logfile", logfile)
            plugin_paths = getattr(namespace, "plugin_paths", plugin_paths)
            plugin_files = getattr(namespace, "plugin_files", plugin_paths)

        # etccore.logger.LoggerCreator
        try:
            rootlogger = init_logger(
                loggername=loggername, log_level=log_level, logfile=logfile)
        except Exception as ex:
            objects.append(ex)
            rootlogger = None
        else:
            objects.append(rootlogger)

        # logging is ready
        if rootlogger is not None:
            logger = rootlogger.getChild(self.loggername)
            if logger.isEnabledFor(logging.DEBUG):
                _log_mex = "Cmd given "

                if plugin_paths:
                    _log_mex += "plugin paths: {} "
                if plugin_files:
                    _log_mex += "files: {}".format(", ".join(plugin_files))

                if _log_mex != "Cmd given ":
                    logger.debug(_log_mex)

        # etccore.confmgr.ConfigFileFactory
        try:
            configfactory = create_configfactory(
                *plugin_paths, plugin_files=plugin_files)
        except Exception as ex:
            objects.append(ex)
        else:
            objects.append(configfactory)

            return objects

    def _anxillary_validator(self, objects: list):
        """
        Validate objects generated by
        :meth:`UiLauncher.init_anxillary_stuffs` method.
        """
        rootlogger = objects[0]
        if isinstance(rootlogger, Exception):
            # No logger available, so print.
            print(
                "!!!!!! CRITICAL ERROR !!!!!!",
                "Failed to create the root logger.",
                "Open an issue to the gitlab repository "
                "(or contact the prettyetc developers) copying this message,"
                "including the traceback below.\n\n",
                " ".join(
                    traceback.format_exception(
                        type(rootlogger), rootlogger,
                        rootlogger.__traceback__)),
                sep="\n",
                file=sys.stderr)
            sys.exit(1)

        else:
            self.logger = rootlogger.getChild(self.loggername)
            self.logger.debug("Created logger")

        configfactory = objects[1]
        if isinstance(configfactory, Exception):
            self.logger.critical(
                "Failed to create the config factory.\n"
                "Open an issue to the gitlab repository\n"
                "(or contact the prettyetc developers) copying this message,\n"
                "including the traceback below.\n\n",
                exc_info=configfactory)
            sys.exit(1)

    def use_ui(self, cls: type,
               configfactory: ConfigFileFactory = None) -> BaseMain:
        """Create and init the UI instance."""
        if configfactory is None:
            args = parse_args()
            objects = self.init_anxillary_stuffs(namespace=args)
            self._anxillary_validator(objects)
            configfactory = objects[1]

        try:
            mainui = cls(configfactory=configfactory)
        except Exception as ex:  # pylint: disable=W0703
            self.logger.error(
                "Failed to instance an object of %s, below the traceback",
                mainui,
                exc_info=ex)
            return None

        # init UI and load cmd-passed paths
        mainui.init_ui()
        for path in args.paths:
            if path is not None:
                path = path if os.path.isabs(path) else os.path.abspath(path)
                mainui.read_file(path)

        return mainui

    def create_ui(self) -> BaseMainUi:
        """
        Create all the required stuffs for creating an UI,
        then fetch all available UIs and looking for a working one.
        So initialize it and dispatch the reading for all paths passed
        by command-line.

        .. todo::
            Use better exit codes than 1 if errors
        """

        args = parse_args()
        objects = self.init_anxillary_stuffs(namespace=args)
        self._anxillary_validator(objects)
        configfactory = objects[1]

        # UI fetch
        self.find_uis()
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(
                "Loaded uis: %s",
                " ".join(cls.__name__ for _, cls in self.loaded_uis))

        self.sort_uis()
        mainui = None
        for _, ui in self.loaded_uis:
            mainui = self.use_ui(ui, configfactory=configfactory)
            if mainui is not None:
                # UI is ready to use
                break
        else:
            self.logger.critical(
                "Failed to create any UI interface\n"
                "Open an issue to the gitlab repository\n"
                "(or contact the prettyetc developers).\n"
                "If there are errors above, please copy it also in the issue\n\n"
                "This program will be closed.")
            sys.exit(1)

        return mainui

    @classmethod
    def main(cls, *args, ui_cls: type = None, **kwargs):
        """
        Launch the UI.

        This method is called by :meth`.BaseMain.main` method,
        that usually called by launch scripts or setuptools generated scripts.
        """

        self = cls(*args, **kwargs)
        if ui_cls is None:
            try:
                mainui = self.create_ui()

                mainui.show()
                mainui.close()
            except Exception as ex:  # pylint: disable=W0703
                self.logger.critical(
                    "\n"
                    "Failed to launch prettyetc.\n"
                    "Open an issue to the gitlab repository"
                    "(or contact the prettyetc developers) copying this message,"
                    "including the traceback below."
                    "Try running the program again with -vvv and if there are errors above, "
                    "please copy them and create an issue on the project repo\n\n"
                    "This program will be closed.\n\n",
                    exc_info=ex)
                sys.exit(1)

        else:
            mainui = self.use_ui(ui_cls)
            if mainui is None:
                print(
                    "Failed to launch {}.{} class.".format(
                        ui_cls.__module__,
                        ui_cls.__name__,
                    ),
                    file=sys.stderr)
                sys.exit(1)
            else:
                mainui.show()
                mainui.close()
