#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module manage configuration files and it find out a good parser to
parse given file.

.. warning::
    Writing config to stream is NOT supported at the moment.
"""

__all__ = ("ConfigStream", "ConfigFile", "ConfigFileFactory")

from . import plugins
from .langlib import RootField, parsers
from .logger import ChildLoggerHelper, errhelper


class ConfigStream(ChildLoggerHelper):
    """Representation of a configuration string, contained in a stream."""

    __slots__ = ("root", "stream")

    loggername = "core.config.stream"

    def __init__(self, stream: open):
        super().__init__()
        self.stream = stream

    def automatch(self,
                  matcher: parsers.FileMatcher,
                  hint: parsers.BaseParser = None
                  ) -> (parsers.BaseParser, RootField):
        """Call all matcher to get right parser."""
        parser, parsed = matcher.try_parser(self.stream, hint)
        if parser is None:
            self.logger.debug("No parser found.")
        return parser, parsed

    def read(self, matcher: parsers.FileMatcher):
        """Read and parse the file using teh properly parser,
        if file is parsed correctly its data is saved into root attribute."""
        parser, root = self.automatch(matcher)
        if root is None:
            if parser is None:
                return errhelper(
                    parsers.BadInput(
                        filename=self.stream.name,
                        is_valid=False,
                        incriminated_string=
                        "No valid parser found for this file.",
                        repr_toargs=True), self.logger)
            try:
                root = parser().parse_file(self.stream)
            except parsers.BadInput as ex:
                return ex

        return root

    def write(self, language: str):
        """Write the root to file using given language."""
        self.logger.info("Writing feature is coming soon.")
        raise NotImplementedError("Writing feature is coming soon.")


class ConfigFile(ConfigStream):
    """Representation of a configuration file."""

    __slots__ = ("filename", )

    def __init__(self, filename: str):
        try:
            stream = open(filename, "r+")
        except OSError:
            stream = open(filename, "w+")
        super().__init__(stream)
        self.filename = filename

    def automatch(self, matcher: parsers.FileMatcher
                  ) -> (parsers.BaseParser, RootField):
        """Call all matcher to get right parser."""
        filename_parser = matcher.match_filename(self.filename)
        parser, parsed = super().automatch(matcher, hint=filename_parser)
        if parser is None:
            self.logger.debug("No parser found, return last known parser.")
            return filename_parser, None
        return parser, parsed


class ConfigFileFactory(object):
    """
    This class provides a centralized way to create ConfigFile objects.

    It initializes and manages all necessary stuffs that will be used to read and write.
    """

    def __init__(self, *plugin_paths: str, plugin_files: list = None):
        super().__init__()
        self.plugin_mgr = plugins.PluginManager()
        self.plugin_mgr.fetch_folder("prettyetc/etccore/langs")
        for path in plugin_paths:
            self.plugin_mgr.fetch_folder(path)
        if hasattr(plugin_files, "__iter__"):
            for path in plugin_files:
                self.plugin_mgr.load_module(path)
        self.matcher = parsers.FileMatcher(self.plugin_mgr)

    def __call__(self, *args, **kwargs) -> RootField:
        """Create and configure a ConfigFile object."""
        configfile = ConfigFile(*args, **kwargs)

        return configfile
