#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module manages configuration files and it looks for a good parser to
parse the given file.
"""

__all__ = ("ConfigStream", "ConfigFile", "ConfigFileFactory")
import inspect
import io
import logging
import os
import tempfile

from . import plugins
from .langlib import RootField
from .langlib.parsers import BadInput, BaseParser, FileMatcher
from .langlib.serializers import SerializeFailed
from .logger import ChildLoggerHelper, LoggerCreator, errhelper


class ConfigStream(ChildLoggerHelper):
    """
    Representation of a configuration string, contained in a stream.

    :param stream:
        A stream that contains the config.
        Should be readable to allows parsing and writable to allows serializing.

    :param prettyetc.etccore.langlib.parsers.FileMatcher matcher:
        The matcher to detect config language used in stream.

        .. versionadded:: 0.2.0

        .. deprecated:: 0.4.0
            All the :class:`~prettyetc.etccore.langlib.parsers.FileMatcher`
            methods and attributes were migrated in this class.
            So, this parameter is maintained for backward compatibility
            and will be used to extract the plugin manager, necessary to
            get parsers and serializers.


    :param prettyetc.etccore.plugins.PluginManager plugin_mgr:
        The plugin manager that contains all the loaded plugins,
        especially parsers and serializers plugins.

        By default, it is None to maintain backward compatibility, however,
        if you don’t provide the plugin manager, the serializer feature will not work.

        .. versionadded:: 0.4.0

    .. versionchanged:: 0.4.0
        Now this class contains all the
        :class:`~prettyetc.etccore.langlib.parsers.FileMatcher` methods.
    """

    __slots__ = ("stream", "plugin_mgr")

    loggername = "etccore.config.stream"

    def __init__(self,
                 stream: io.IOBase,
                 matcher: FileMatcher = None,
                 plugin_mgr: plugins.PluginManager = None):
        super().__init__()
        self.stream = stream
        """
        I/O stream for reading and writing the config.
        This will be passed to :class:`.BaseParser` and :class:`.BaseSerializer` objects.
        """

        if matcher and plugin_mgr is None:
            plugin_mgr = matcher.mgr
        self.plugin_mgr = plugin_mgr
        if self.plugin_mgr is None:
            self.logger.warning(
                "No PluginManager isinstance given, the write method will throw an unexpected error"
            )

    def __enter__(self):
        """
        Create a context manager.

        By default it does nothing.

        .. versionadded:: 0.4.0
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit from the context manager.

        By default it does nothing.

        .. versionadded:: 0.4.0
        """

    # from deprecated FileMatcher
    def get_language(self, language: str, type_: str = "parser") -> BaseParser:
        """
        Get the first occurrence of lang searching in plugin lists.

        If no plugin is found, it will return None.
        """
        language = language.lower()
        if type_ == "parser":
            for parser in self.plugin_mgr.loaded_parsers.values():
                if language in parser.LANGUAGES:
                    return parser

        elif type_ in ("serializer", "writer"):
            return self.plugin_mgr.loaded_serializers.get(language)

        return None

    def match_filename(self, path: str) -> BaseParser:
        """
        Find the properly parser by given path to file.

        This method in particular locking for file names, especially
        suffixes, if no parser has been found, call the :meth:`ConfigStream.try_parser`
        method.

        .. warning::
            This method doesn't guarantee that the given file is valid.
        """
        for parser in self.plugin_mgr.loaded_parsers.values():
            for suffix in parser.SUFFIXES:
                if path.endswith(suffix):
                    self.logger.debug(
                        "Found parser %s for %s file, using match_filename.",
                        parser.__name__, path)
                    return parser
            for prefix in parser.PREFIXES:
                if path.startswith(prefix):
                    self.logger.debug(
                        "Found parser %s for %s file, using match_filename.",
                        parser.__name__, path)
                    return parser
        return None

    def try_parser(self, file: io.IOBase,
                   hint: BaseParser = None) -> (BaseParser, RootField):
        """Try to parse the file, if parsing is successful, returns the
        parser and the parsed content."""
        parsers = list(self.plugin_mgr.loaded_parsers.values())
        if hint is not None and issubclass(hint, BaseParser):
            try:
                parser_inst = hint()
                parsed = parser_inst.parse_file(file)

            except BadInput:
                if hasattr(file, "name"):
                    self.logger.debug("Parser %s isn't valid for file %s.",
                                      hint.__name__, file.name)
                else:
                    self.logger.debug("Parser %s isn't valid for that stream",
                                      hint.__name__, file.name)
            except IOError as ex:
                self.logger.warning(
                    "An error occurred while reading the file.\nReason:",
                    exc_info=ex)

                raise BadInput(
                    filename=ex.filename,
                    is_valid=False,
                    reason="An error occurred while reading the file.",
                    original_exc=ex)

            else:
                return hint, parsed
            file.seek(0)
            parsers.remove(hint)

        used_parsers = set()
        for parser in parsers:
            if parser in used_parsers:
                continue
            used_parsers.add(parser)
            try:
                temp_parser = parser()
                parsed = temp_parser.parse_file(file)

            except BadInput:
                self.logger.debug("Parser %s isn't valid for that file.",
                                  parser.__name__)
            except IOError as ex:
                self.logger.warning(
                    "An error occurred while reading the file.\nReason:",
                    exc_info=ex)

                raise BadInput(
                    filename=ex.filename,
                    is_valid=False,
                    reason="An error occurred while reading the file.",
                    original_exc=ex)

            else:
                return parser, parsed
            file.seek(0)

        return None, None

    def automatch(self, hint: BaseParser = None) -> (BaseParser, RootField):
        """Call all matcher to get the right parser."""
        parser, parsed = self.try_parser(self.stream, hint)
        if parser is None:
            self.logger.debug("No parser found.")
        return parser, parsed

    def read(self, matcher: FileMatcher = None):
        """
        Read the file and parse its content using the properly parser,
        if file is parsed correctly its data is saved into root attribute.

        :param prettyetc.etccore.langlib.parsers.FileMatcher matcher:
            The matcher to use for reading.

            .. deprecated:: 0.2.0
                All the :class:`.FileMatcher` members were migrated in this class.
                So the use of :class:`.FileMatcher` is highly discouraged.

        :return: a :class:`.RootField` object if a valid parser is found.

        :rtype: RootField

        :return: a :class:`.BadInput` object if any error occurred
                 while parsing or no valid parser is found.

        :rtype: BadInput

        :raises NotImplementedError: If :attr:`ConfigStream.stream` is not readable.
        """
        if self.stream is None:
            return BadInput(reason="Missing or empty stream.", is_valid=False)
        if not getattr(self.stream, "readable", lambda: False)():
            raise errhelper(
                NotImplementedError("Can't read from given stream"),
                self.logger)

        if matcher is None:
            parser, root = self.automatch()
        else:
            parser, root = matcher.automatch()

        if root is None:
            if parser is None:
                return errhelper(
                    BadInput(
                        filename=self.stream.name,
                        is_valid=False,
                        reason="No valid parser found for this file.",
                        repr_toargs=True,
                    ),
                    self.logger,
                )
            try:
                root = parser().parse_file(self.stream)
            except BadInput as ex:
                return ex

        return root

    def write(self, rootfield: RootField, language: str, **serializer_settings):
        """
        Serialize the root to :attr:`~.ConfigStream.stream`
        using given language and write it into the stream.

        :param RootField rootfield: the rootfield to be serialized

        :param str language: the language to convert the rootfield.
                             a serializer for it must be loaded in the plugin manager
                             or a :class:`.SerializeFailed` exception will be raised.

        :raises SerializeFailed: If serializing fails during the
                                 :class:`.RootField` object conversion to language code.

        :raises SerializeFailed: If the given rootfield is not a :class:`.RootField` object.

        :raises NotImplementedError: If :attr:`.ConfigStream.stream` is not writable.

        .. versionchanged:: 0.4.0
            Method implemented.
            It no longer raises a NotImplementedError.
        """
        if isinstance(rootfield, Exception):
            raise SerializeFailed(
                reason="Can't serialize a {} object.".format(
                    type(rootfield).__name__),
                original_exc=rootfield)
        if self.stream is None:
            raise SerializeFailed(reason="Missing or empty stream.")

        if not getattr(self.stream, "writable", lambda: False)():
            raise errhelper(
                NotImplementedError("Can't write to given stream"),
                self.logger,
            )
        serializer = self.get_language(language, "serializer")
        if serializer is None:
            raise errhelper(
                SerializeFailed(
                    filename=self.stream.name,
                    reason="No valid serializer found for this language.",
                    repr_toargs=True,
                ),
                self.logger,
            )
        writerinst = serializer(**serializer_settings)
        writerinst.serialize_file(rootfield, self.stream)

    parse = read
    """A shorthand for :meth:`~ConfigStream.read`."""

    serialize = write
    """A shorthand for :meth:`~ConfigStream.write`."""


class ConfigFile(ConfigStream):
    """Representation of a configuration file."""

    __slots__ = ("filename",)

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

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Flush and close the file stream, in any case.

        This does not suppress the exception.

        .. versionadded:: 0.4.0
        """
        self.stream.close()

    def read(self, *args, **kwargs):
        res = super().read(*args, **kwargs)
        if self.stream is None and isinstance(res, BadInput):
            res.filename = self.filename
            res.reason = "Can't read the file: Permission denied"
        return res

    def write(self, rootfield: RootField, *args, flush: bool = False, **kwargs):
        """
        Truncate the file before serializing and, if any error occurred
        restore the old source.

        :param bool flush: If True, call :meth:`~io.IOBase.flush` after writing.

        .. seealso::
            :meth:`.ConfigStream.write` for the usage.

        .. versionadded:: 0.4.0
        """
        if isinstance(rootfield, BadInput):
            super().write(rootfield, language=None)
        old_content = rootfield.source
        try:
            self.stream.seek(0)
            self.stream.truncate()
        except io.UnsupportedOperation:
            # TODO: raise an exception and document it
            pass
        else:
            try:
                super().write(rootfield, *args, **kwargs)
                if flush:
                    self.stream.flush()
            except Exception as ex:
                self.stream.truncate()
                self.stream.write(old_content)
                raise ex

    def automatch(  # pylint: disable=W0613
            self, matcher: FileMatcher = None) -> (BaseParser, RootField):
        """
        Call all matcher to get right parser.

        :param prettyetc.etccore.langlib.parsers.FileMatcher matcher:
            The matcher to detect config language used in stream.

            .. deprecated:: 0.4.0
                All the :class:`~prettyetc.etccore.langlib.parsers.FileMatcher`
                are migrated in :class:`~ConfigStream` class, so this parameter is useless.
        """
        filename_parser = self.match_filename(self.filename)
        parser, parsed = super().automatch(hint=filename_parser)
        if parser is None:
            self.logger.debug("No parser found, return last known parser.")
            if filename_parser is not None:
                self.logger.debug("Last known parser is match_filename parser.")
                # filename matches is the preferred error.
                self.stream.seek(0)
                try:
                    parsed = filename_parser().parse_file(self.stream)
                except BadInput as ex:
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
    This class provides a centralized way to create
    :class:`~ConfigFile` and :class:`~ConfigStream` objects.

    It initializes and manages allb the necessary stuffs that will be used to read and write.

    :param type configfile_class: A subclass of :class:`~ConfigFile`
                                  to use to create file objects.

    :param type configstream_class: A subclass of :class:`~ConfigStream`
                                    to use to create stream objects.

    :param bool enable_logger: If True, :class:`~ConfigFileFactory`
                               creates for you a logger for prettyetc.
    """
    loggername = "etccore.config.factory"

    def __init__(self,
                 *plugin_paths: str,
                 plugin_files: list = None,
                 configfile_class: type = ConfigFile,
                 configstream_class: type = ConfigStream,
                 enable_logger: bool = False,
                 logger_level: int = logging.WARNING):

        # logging init
        if enable_logger and LoggerCreator.ROOT_LOGGER == logging.root:
            temp = tempfile.TemporaryFile(
                prefix="prettyetc-", suffix=".log", mode="w+")
            root = LoggerCreator(
                logging.getLogger("prettyetc"),
                log_level=logger_level,
                logfile=temp,
                root=True)

            if getattr(temp, "name", None) is not None:
                root.getChild("logger").warning(
                    "Use a temporary file to save the log")

        super().__init__()
        self.configfile_class = configfile_class
        self.configstream_class = configstream_class
        self.plugin_mgr = plugins.PluginManager()

        # plugin manager init
        path = os.path.dirname(inspect.getfile(inspect.currentframe()))
        path = os.path.dirname(path)
        path = os.path.join(path, "etccore", "langs")
        self.logger.debug("Default directory for langs plugin: %s", path)
        self.plugin_mgr.search_modules(paths=[path])

        # plugins loading
        for path in plugin_paths:
            self.plugin_mgr.fetch_folder(path)
        if hasattr(plugin_files, "__iter__"):
            for path in plugin_files:
                self.plugin_mgr.load_module(path)

    def __call__(self, *args, **kwargs) -> ConfigFile:
        """A shorthand for :meth:`~ConfigFileFactory.create_file`."""
        if args and isinstance(args[0], io.IOBase):
            return self.create_stream(*args, **kwargs)
        return self.create_file(*args, **kwargs)

    def create_file(self, filename: str, *args, **kwargs) -> ConfigFile:
        """
        Create and configure a ConfigFile object

        All given parameters will be passed to
        :class:`~ConfigFile` in construction.

        .. versionadded:: 0.2.0
        """
        kwargs.setdefault("plugin_mgr", self.plugin_mgr)
        configfile = self.configfile_class(filename, *args, **kwargs)
        return configfile

    def create_stream(self, filename: str, *args, **kwargs) -> ConfigFile:
        """
        Create and configure a ConfigStream object

        All given parameters will be passed to
        :class:`~ConfigStream` in construction.

        .. warning::
            It is discouraged to use this method if the stream can be created by :func:`open`.
            :class:`~ConfigFile` makes extra controls for you not to get unwanted errors.

        .. versionadded:: 0.4.0

        """
        kwargs.setdefault("plugin_mgr", self.plugin_mgr)
        configfile = self.configstream_class(filename, *args, **kwargs)
        return configfile

    def all_language_suffixes(self,
                              type_: str = "parser",
                              only_first_language: bool = True) -> list:
        """
        Get a list of language suffixes pairs.

        :param str type_: The type of plugins to get the suffixes.

            The values supported are:

            - parser (default) for parser plugins
            - serializer for serializer plugins

        :param bool only_first_language:
            If True, for each parser will be added only one language,
            the first in the LANGUAGES attribute.
            Otherwise, if False, all of the parsers language will be added.

        .. versionadded:: 0.4.0
        """
        retlist = []
        if type_ == "parser":
            for parser in self.plugin_mgr.loaded_parsers.values():
                if only_first_language:
                    retlist.append((parser.LANGUAGES[0], parser.SUFFIXES))
                else:
                    for language in parser.LANGUAGES:
                        retlist.append((language, parser.SUFFIXES))

        elif type_ == "serializer":
            for serializer in self.plugin_mgr.loaded_serializers.values():
                if only_first_language:
                    retlist.append((serializer.LANGUAGES[0],
                                    (serializer.STANDARD_EXTENSION,)))
                else:
                    for language in serializer.LANGUAGES:
                        retlist.append((language,
                                        (serializer.STANDARD_EXTENSION,)))

        return retlist
