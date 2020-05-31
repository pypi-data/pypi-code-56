#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains some abstract classes for the main ui manager."""

import argparse
import inspect
import logging
import os
import sys
import traceback

from prettyetc.etccore.langlib.parsers import BadInput
from prettyetc.etccore.logger import DEBUG2
from prettyetc.etccore.plugins import PluginManager

from .cmdargs import parse_args
from .utils import create_configfactory, init_logger, open_callback

__all__ = ("BaseMainUi", "UiLauncher")


class BaseMainUi(object):
    """
    Represents the main instance of an ui.

    It defines a set of abstract methods that provide a basic abstract
    interface.
    """

    def __init__(
            self,
            *args,
            read_callback=lambda *args: None,
            # write_callback=lambda *args: None,
            close_callback=lambda *args: None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.read_callback = read_callback
        # self.write_callback = write_callback
        self.close_callback = close_callback

    if sys.version_info.minor >= 6:

        def __init_subclass__(cls, check_abstract: bool = True, **kwargs):
            """Check if abstract methods are implemented."""
            # NOTE: logger require an instanced LoggerCreator object
            # that is not avaiable in class definitions
            # so root logger is logging.root
            # childlogger_helper(cls.loggername, cls)
            # cls.logger.debug("Subclass method check: %s", cls.__name__)  # pylint: disable=E1101
            if check_abstract and (
                    cls.init_ui == BaseMainUi.init_ui
                    or cls.handle_badinput == BaseMainUi.handle_badinput
                    or cls.show == BaseMainUi.show
                    or cls.add_root == BaseMainUi.add_root):
                raise TypeError(
                    "Can't instantiate abstract class {} with unimplemented methods.".
                    format(BaseMainUi.__name__))

            super().__init_subclass__(**kwargs)

    def init_ui(self):
        """
        Initialize ui, it creates the basic structures for the ui.

        .. note::
            This method is not called in __init__.
        """
        raise NotImplementedError("Method init_ui must be implemented.")

    def handle_badinput(self, path, badinput_ex: BadInput):
        """Handle bad input by given BadInput exception."""
        raise NotImplementedError(
            "Method handle_badinput must be implemented.")

    def show(self):
        """Show the ui to user, must be a blocking call."""
        raise NotImplementedError("Method show must be implemented.")

    def add_root(self, root):
        """Add given root field to ui."""
        raise NotImplementedError("Method add_root must be implemented.")

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
            self.logger.info(
                "Skipping module %s as not contains a valid ui reference.",
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

    def init_anxillary_stuffs(  # pylint: disable=W0703
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
        else:
            objects.append(rootlogger)

        # etccore.confmgr.ConfigFileFactory
        try:
            configfactory = create_configfactory(
                *plugin_paths, plugin_files=plugin_files)
        except Exception as ex:
            self.logger.error("")
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
        Run main program, it should select the UI based on cmd arguments.

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
                "including the traceback below.",
                " ".join(
                    traceback.format_exception(
                        type(rootlogger), rootlogger,
                        rootlogger.__traceback__)),
                sep="\n")
            exit(1)

        else:
            self.logger = rootlogger.getChild(self.loggername)
            self.logger.debug("Created logger")

        configfactory = objects[1]
        if isinstance(configfactory, Exception):
            self.logger.critical(
                "Failed to create the config factory.\n"
                "Open an issue to the gitlab repository\n"
                "(or contact the prettyetc developers) copying this message,\n"
                "including the traceback below.",
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
                mainui = ui(configfactory, read_callback=open_callback)
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
        for path in args.paths:
            # print(args.paths, path)
            if path is not None and not os.path.isabs(path):
                path = os.path.abspath(path)
                mainui.read_callback(mainui, path, configfactory)
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
            mainui.init_ui()
            mainui.show()
        except Exception as ex:  # pylint: disable=W0703
            self.logger.critical(
                "Failed to launch prettyetc\n"
                "Open an issue to the gitlab repository\n"
                "(or contact the prettyetc developers) copying this message,\n"
                "including the traceback below.",
                "If there are errors above, please copy it also in the issue.\n\n"
                "This program will be closed.",
                exc_info=ex)
            exit(1)
