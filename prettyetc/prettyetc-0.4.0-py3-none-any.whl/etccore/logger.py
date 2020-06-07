#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide stuffs for creating a good logging system, using std logging lib."""

import logging
import sys

__all__ = ("DEBUG2", "LoggerCreator", "errhelper", "childlogger_helper",
           "ChildLoggerHelper")
DEBUG2 = 11  # suppress all 3rd party libraries debug


class LevelFilter(logging.Filter):
    """Filter to allow only a level."""

    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """Check if record match the level."""
        return record.levelno == self.level or record.levelname == self.level


class LoggerCreator(object):
    """
    The logger initializer.

    It configures given logger to add features listed below.
    Given logger should to be the root logger of the program.
    Added logging features:

    - set given level to given logger.
    - log in file and stdout with different formatting.
    - (for stdout) use colors.
    """

    ROOT_LOGGER = logging.root

    def __init__(self,
                 logger: logging.Logger,
                 logfile="prettyetc.log",
                 allow_print: bool = True,
                 allow_color: bool = True,
                 log_level: int = logging.WARNING,
                 root: bool = True):
        super().__init__()
        # init self
        self.logger = logger
        if root:
            LoggerCreator.ROOT_LOGGER = self
            logger.propagate = True

        logger.setLevel(log_level)

        # init logger for new features

        # add new levels
        logging.addLevelName(DEBUG2, "DEBUG2")

        # create file handler & formatter
        if logfile is not None:
            if isinstance(logfile, (str, bytes)):
                handler = logging.FileHandler(
                    filename=logfile, encoding='utf-8', mode='w')
            else:
                handler = logging.StreamHandler(logfile)

            handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s:%(name)s::%(levelname)s: %(message)s'))
            logger.addHandler(handler)

        # create console handlers
        if allow_print:
            self.create_print_handlers(allow_color)

        # logging shorthands methods
        self.debug = logger.debug
        self.info = logger.info
        self.warning = logger.warning
        self.error = logger.error
        self.exception = logger.exception
        self.critical = logger.critical
        self.log = logger.log
        self.getChild = logger.getChild
        self.setLevel = logger.setLevel

    def debug2(self, msg: str, *args, **kwargs):
        """Shorthand of logger.log(DEBUG2)."""
        self.logger.log(DEBUG2, msg, *args, **kwargs)

    def create_print_handlers(self, allow_color: bool = True):
        """Create logger for console, with colors if allow_color is True."""
        if allow_color:
            # color levels initialization
            for color, level in ((31, logging.CRITICAL), (32, logging.INFO),
                                 (33, logging.WARNING), (35, logging.ERROR),
                                 (36, logging.DEBUG), (36, DEBUG2)):
                stream = sys.stdout if level < logging.WARNING else sys.stderr
                handler = logging.StreamHandler(stream=stream)
                handler.addFilter(LevelFilter(level, name=self.logger.name))
                handler.setFormatter(
                    logging.Formatter(
                        '[\033[{};1;1m%(levelname)s\033[0m]:%(name)s: %(message)s'.
                        format(color)))
                self.logger.addHandler(handler)
        else:
            # standard levels initialization
            for level in (logging.CRITICAL, logging.INFO, logging.WARNING,
                          logging.ERROR, logging.DEBUG, DEBUG2):
                stream = sys.stdout if level < logging.WARNING else sys.stderr
                handler = logging.StreamHandler(stream=stream)
                handler.setLevel(level)
                handler.setFormatter(
                    logging.Formatter('%(levelname)s: %(message)s'))
                self.logger.addHandler(handler)


# class shorthands that you SHOULD use
class ChildLoggerHelper(object):
    """
    This class provides the same feature of :func:`~childlogger_helper`
    function, but at __init__ level.

    It requires the loggername attribute to be setted to the desired logger name.
    """

    logger = None
    loggername = None

    def __init__(self, *args, **kwargs):
        self.init_logger()
        super().__init__(*args, **kwargs)

    def init_logger(self) -> None:
        """
        Initialize the object logger, called by __init__.

        This method should be used only if you need logger before calling super.
        """
        if self.loggername is None:
            raise ValueError("loggername attribute must be setted.")
        childlogger_helper(self.loggername, type(self), self)


# function shorthands that you SHOULD use
def errhelper(exc: Exception, logger: logging.Logger,
              msg: str = "") -> Exception:
    """
    This helper functions log given exception. in given logger and return the exception.

    This is intended as shorthands to join 3 lines into just 1 like that:

    .. code::

        ex = Exception("message")
        logger.error(exc_info=ex)
        raise ex

    **Into** :

    .. code::

        raise errhelper(Exception("message"), logger)
    """
    logger.error(msg, exc_info=exc)
    return exc


def childlogger_helper(childlogger: str, cls: type,
                       self=None) -> logging.Logger:
    """
    This helper functions return a sublogger and assign it to given cls and object of self (if given).
    This is intended as shorthands to join 2 or 3 lines into just 1 like these.

    When self is None:

    .. code::

      if cls.logger is None:
          cls.logger = LoggerCreator.ROOT_LOGGER.getChild(childlogger)

    When self is not None:

    .. code::

        if cls.logger is None:
            cls.logger = LoggerCreator.ROOT_LOGGER.getChild(childlogger)
            self.logger = cls.logger

    **Into** :

    .. code::

        childlogger_helper("some.logger", cls)
        # or
        childlogger_helper("some.logger", cls, self)

    .. note::
        No controls is done to check if self is an instance of cls.
    """
    if getattr(cls, "logger", None) is None:
        cls.logger = LoggerCreator.ROOT_LOGGER.getChild(childlogger)
        if self is not None:
            self.logger = cls.logger
    return cls.logger
