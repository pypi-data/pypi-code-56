#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains some abstract classes for the main ui manager."""

import abc
import argparse
import inspect
import logging
import os
import sys
import traceback

from prettyetc.etccore.confmgr import ConfigFileFactory
from prettyetc.etccore.langlib.parsers import BadInput
from prettyetc.etccore.langlib.root import RootField
from prettyetc.etccore.logger import DEBUG2, ChildLoggerHelper, errhelper
from prettyetc.etccore.plugins import PluginManager

from .cmdargs import parse_args
from .utils import create_configfactory, init_logger

__all__ = ("BaseMainUi", "UiLauncher")


class BaseMainUi(ChildLoggerHelper, metaclass=abc.ABCMeta):
    """
    Represents the main instance of an ui.

    It defines a set of abstract methods that provide a basic abstract
    interface.

    :param :class:`~prettyetc.etccore.confmgr.ConfigFileFactory` configfactory:
        The config factory.


    :param callable read_callback:

        A callable object called when a config file is open.
        It should open the file at path and process it
        through the parsers (or the file matcher).

        .. deprecated:: 0.2.0
            Use predefined :meth:`~BaseMainUi.open_config_file` instead

    :param callable close_callback:

        Removed in 0.2.0: This parameter never works.

    .. versionchanged:: 0.2.0
        Now this class inhiterits :class:`abc.ABC`
        and all the abstract methods are decorated
        with :func:`abc.abstractmethod`.
    """

    def __init__(
            self,
            *args,
            configfactory: ConfigFileFactory = None,

            # deprecated
            read_callback=None,
            **kwargs):
        super().__init__(*args, **kwargs)

        if configfactory is None and read_callback is None:
            raise ValueError("A ConfigFileFactory object must be given.")
        self.configfactory = configfactory

        # deprecated
        self.read_callback = read_callback

    def open_config_file(self, path):
        """The open_config_file method."""
        if self.read_callback is None:
            configfile = self.configfactory(path)
            root = configfile.read()
            if isinstance(root, BadInput):
                self.handle_badinput(path, root)
            elif isinstance(root, RootField):
                self.add_root(root)
            else:
                raise errhelper(TypeError("Bad root returned"), self.logger)
        else:
            # deprecated
            self.read_callback(self, path, self.configfactory)

    @abc.abstractmethod
    def init_ui(self):
        """
        Initialize ui, it creates the basic structures for the ui.

        .. note::
            This method is not called in __init__.
        """

    @abc.abstractmethod
    def show(self):
        """Show the ui to user, must be a blocking call."""

    @abc.abstractmethod
    def add_root(self, root):
        """Add given :class:`~prettyetc.etccore.langlib.root.RootField` object to ui."""

    @abc.abstractmethod
    def handle_badinput(self, path, badinput_ex: BadInput):
        """Handle bad input by given :exc:`~prettyetc.etccore.langlib.parsers.BadInput`."""

    @classmethod
    def main(cls, *args, **kwargs):
        """Launch the ui, using the UiLauncher."""


class UiLauncher(PluginManager):
    """
    This class scan the prettyetc directory to find launchable uis
    and provide a convenient way to launch it.

    A valid ui is a module (or a package with an __init__.py module)
    where there are at least 2 these attributes
    (inserted into the __all__ attrubute if exists):

    - __prettyetc_ui__
        Contains the name of the ui.
        It is used for preferring an ui (via the preferred_uis attribute).
        This name is not unique, (and should not) because the name could
        contain information about Ui library used, for example.
    - __main_class__
        This class **must** be a subclass of BaseMainUi and its signature
        must be the same (plus extra keyword arguments if you want)
        in order to launch the UI.

    These attributes are used BOTH to launch an ui.
    """

    loggername = "baseui.main.loader"

    def __init__(self, preferred_uis: tuple = ()):
        # do not use logging here since it is not ready
        super().__init__()
        self.preferred_uis = preferred_uis
        self.loaded_uis = []
        del self.loaded_parsers

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
        if uiclass is None or uiname is None:
            self.logger.log(
                11, "Skipping module %s as not contains a valid ui reference.",
                mod.__name__)
        else:
            self.load_plugin(uiname, uiclass)

    def find_uis(self, path: str = None):
        """Scan the prettyetc directory (or the given one) to find a valid ui."""
        if path is None:
            path = os.path.dirname(inspect.getfile(inspect.currentframe()))
            path = os.path.dirname(path)
        self.logger.debug("Load UIs from %s", path)
        # load both directories and modules
        self.fetch_folder(path, only_dirs=True)
        self.fetch_folder(path)

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
        (according to cmdargs.create_parser function).

        It create and manage (if necessary) all classes and objects
        that would be created before doing anything else.

        Classes and object managed
        (see classes and modules documentation for more details about these listed classes)


        - :class:`~etccore.logger.LoggerCreator` (via :func:`~baseui.utils.init_logger`)

         The logger inizializer.
         Can be configured with:

          - logging level
          - root logger name
          - log path

        - :class:`~etccore.confmgr.ConfigFileFactory` (via :func:`~baseui.utils.create_configfactory`)

         It inizialize the configfile object factory.
         The config factory also inizialize the plugin manager
         and the file matcher (using the plugin manager instance).
         Can be configured with:

          - plugin paths
          - plugin modules

        This function return all the objects created.
        The order of returned objects is the same of listed classes above.

        .. warning ::
            If one of object fail to be created,
            an exception is provide instead of the expected objects.
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

    def sort_uis(self):
        """
        Sort the ui list by preferred_uis.
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

    def create_ui(self) -> BaseMainUi:
        """
        Create and init the first avaiable ui.

        This method build and init an ui from
        command-line arguments.

        .. todo::
            Use better exit codes than 1 if errors
        """

        args = parse_args()
        objects = self.init_anxillary_stuffs(namespace=args)

        rootlogger = objects[0]
        if isinstance(rootlogger, Exception):
            # No logger avaiable, so print.
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
            exit(1)

        else:
            self.logger = rootlogger.getChild(self.loggername)
            self.logger.debug("Created logger")

        self.logger.debug("Parsed cmd arguments: {}".format(args))

        configfactory = objects[1]
        if isinstance(configfactory, Exception):
            self.logger.critical(
                "Failed to create the config factory.\n"
                "Open an issue to the gitlab repository\n"
                "(or contact the prettyetc developers) copying this message,\n"
                "including the traceback below.\n\n",
                exc_info=configfactory)
            exit(1)

        # ui fetch
        self.find_uis()
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(
                "Loaded uis: %s",
                " ".join(klass.__name__ for _, klass in self.loaded_uis))

        self.sort_uis()
        mainui = None
        for _, ui in self.loaded_uis:
            try:
                mainui = ui(configfactory=configfactory)
            except Exception as ex:  # pylint: disable=W0703
                mainui = None
                self.logger.error(
                    "Failed to instance an object of %s, below the traceback",
                    mainui,
                    exc_info=ex)
            else:
                # ui is ready to use
                break

        if mainui is None:
            self.logger.critical(
                "Failed to create the Ui interface\n"
                "Open an issue to the gitlab repository\n"
                "(or contact the prettyetc developers).\n"
                "If there are errors above, please copy also it in the issue\n\n"
                "This program will be closed.")
            exit(1)

        # init ui and load cmd-passed paths
        mainui.init_ui()
        for path in args.paths:
            if path is not None and not os.path.isabs(path):
                path = os.path.abspath(path)
                mainui.open_config_file(path)
                # mainui.read_callback(mainui, path, configfactory)

        return mainui

    @classmethod
    def main(cls, *args, **kwargs):
        """
        Launch main ui.

        This method is called by setuptools generated script.
        """

        self = cls(*args, **kwargs)
        try:
            mainui = self.create_ui()

            mainui.show()
        except Exception as ex:  # pylint: disable=W0703
            self.logger.critical(
                "\n"
                "Failed to launch prettyetc\n"
                "Open an issue to the gitlab repository\n"
                "(or contact the prettyetc developers) copying this message,\n"
                "including the traceback below.\n"
                "If there are errors above, please copy it also in the issue.\n\n"
                "This program will be closed.\n\n",
                exc_info=ex)
            exit(1)
