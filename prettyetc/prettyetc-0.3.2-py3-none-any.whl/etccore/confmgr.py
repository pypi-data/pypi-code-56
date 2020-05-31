#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module manage configuration files and it find out a good parser to
parse given file.

.. warning::
    Writing feature is NOT supported at the moment.
"""

__all__ = ("ConfigStream", "ConfigFile", "ConfigFileFactory")
import inspect
import os

from . import plugins
from .langlib import RootField, parsers
from .langlib.parsers import BadInput
from .logger import ChildLoggerHelper, errhelper


class ConfigStream(ChildLoggerHelper):
    """
    Representation of a configuration string, contained in a stream.

    :param stream: a stream that contains the config.

    :param :class:`~prettyetc.etccore.langlib.parsers.FileMatcher` matcher:
        The matcher to detect config language used in stream.

        .. versionadded:: 0.2.0
    """

    __slots__ = ("stream", "matcher")

    loggername = "etccore.config.stream"

    def __init__(self, stream: open, matcher: parsers.FileMatcher = None):
        super().__init__()
        self.stream = stream
        self.matcher = matcher

    def automatch(self,
                  matcher: parsers.FileMatcher,
                  hint: parsers.BaseParser = None
                  ) -> (parsers.BaseParser, RootField):
        """Call all matcher to get right parser."""
        parser, parsed = matcher.try_parser(self.stream, hint)
        if parser is None:
            self.logger.debug("No parser found.")
        return parser, parsed

    def read(self, matcher: parsers.FileMatcher = None):
        """
        Read and parse the file using teh properly parser,
        if file is parsed correctly its data is saved into root attribute.

        :param :class:`~prettyetc.etccore.langlib.parsers.FileMatcher` matcher:
            The matcher to use for reading.

            .. deprecated:: 0.2.0
                Use instance matcher instead
        """
        if self.stream is None:
            return BadInput(reason="Missing or empty stream.", is_valid=False)

        # 0.1.x compatibility
        if matcher is None:
            matcher = self.matcher

        parser, root = self.automatch(matcher)
        if root is None:
            if parser is None:
                return errhelper(
                    BadInput(
                        filename=self.stream.name,
                        is_valid=False,
                        reason="No valid parser found for this file.",
                        repr_toargs=True), self.logger)
            try:
                root = parser().parse_file(self.stream)
            except BadInput as ex:
                return ex

        return root

    def write(self, language: str):
        """Write the root to file using given language."""
        self.logger.info("Writing feature is coming soon.")
        raise NotImplementedError("Writing feature is coming soon.")


class ConfigFile(ConfigStream):
    """Representation of a configuration file."""

    __slots__ = ("filename", )

    loggername = "etccore.config.file"

    def __init__(self, filename: str, **kwargs):
        self.init_logger()
        try:
            stream = open(filename, "r+")
            self.logger.debug("File %s opened in both read and write mode",
                              filename)

        except PermissionError:
            try:
                stream = open(filename, "r")
                self.logger.warning("File %s opened in read only mode",
                                    filename)
            except PermissionError:
                self.logger.error(
                    "Failed to open file %s in readonly mode due to missing permissions.",
                    filename)
                stream = None

        except FileNotFoundError:
            stream = open(filename, "w+")
            self.logger.info(
                "File %s didn't exists, a new empty file will be created.",
                filename)

        except IsADirectoryError as ex:
            raise errhelper(ex, self.logger)

        if stream is not None:
            self.logger.debug("Open given file %s in %s mode", filename,
                              stream.mode)

        super().__init__(stream, **kwargs)
        self.filename = filename

    def read(self, *args, **kwargs):
        res = super().read(*args, **kwargs)
        if self.stream is None and isinstance(res, BadInput):
            res.filename = self.filename
            res.reason = "Can't read the file: Permission denied"
        return res

    def automatch(self, matcher: parsers.FileMatcher
                  ) -> (parsers.BaseParser, RootField):
        """Call all matcher to get right parser."""
        filename_parser = matcher.match_filename(self.filename)
        parser, parsed = super().automatch(matcher, hint=filename_parser)
        if parser is None:
            self.logger.debug("No parser found, return last known parser.")
            if filename_parser is not None:
                self.logger.debug(
                    "Last known parser is match_filename parser.")
                # filename matches is the preferred error.
                self.stream.seek(0)
                try:
                    parsed = filename_parser().parse_file(self.stream)
                except parsers.BadInput as ex:
                    return filename_parser, ex
                else:
                    self.logger.debug(
                        "The parser {} works when it wants".format(
                            filename_parser.__name__))
                    return filename_parser, parsed
            return filename_parser, None
        return parser, parsed


class ConfigFileFactory(ChildLoggerHelper):
    """
    This class provides a centralized way to create ConfigFile objects.

    It initializes and manages all necessary stuffs that will be used to read and write.
    """
    loggername = "etccore.config.factory"

    def __init__(self, *plugin_paths: str, plugin_files: list = None):
        super().__init__()
        self.plugin_mgr = plugins.PluginManager()

        path = os.path.dirname(inspect.getfile(inspect.currentframe()))
        path = os.path.dirname(path)
        path = os.path.join(path, "etccore", "langs")
        self.logger.debug("Default directory for langs plugin: %s", path)
        self.plugin_mgr.fetch_folder(path)

        for path in plugin_paths:
            self.plugin_mgr.fetch_folder(path)
        if hasattr(plugin_files, "__iter__"):
            for path in plugin_files:
                self.plugin_mgr.load_module(path)
        self.matcher = parsers.FileMatcher(self.plugin_mgr)

    def create_file(self, *args, **kwargs) -> ConfigFile:
        """
        Create and configure a ConfigFile object

        All given parameters all passed to
        :class:`~ConfigFile` in construction.

        .. versionadded:: 0.2.0
        """
        kwargs.setdefault("matcher", self.matcher)
        configfile = ConfigFile(*args, **kwargs)
        return configfile

    def __call__(self, *args, **kwargs) -> ConfigFile:
        """A shorthand for :meth:`~ConfigFileFactory.create_file`."""
        return self.create_file(*args, **kwargs)
