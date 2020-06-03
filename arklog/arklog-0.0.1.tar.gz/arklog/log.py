from typing import Callable

import yaml
import logging
from functools import wraps, partial
import pathlib

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
EXTRA = 15
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


class ColorFormatter(logging.Formatter):
    """Formatter supporting colors."""
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    ORANGE = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHTGRAY = "\033[0;37m"
    DARKGRAY = "\033[1;30m"
    LIGHTRED = "\033[1;31m"
    LIGHTGREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHTBLUE = "\033[1;34m"
    LIGHTPURPLE = "\033[1;35m"
    LIGHTCYAN = "\033[1;36m"
    WHITE = "\033[1;37m"
    NC = "\033[0m"

    COLORS = {
        DEBUG: BLUE,
        EXTRA: GREEN,
        INFO: WHITE,
        WARNING: YELLOW,
        ERROR: LIGHTRED,
        CRITICAL: RED,
    }

    def format(self, record) -> str:
        """Same as logging.Formatter except it now adds color."""
        color = self.COLORS[record.levelno]
        return f"{color}{logging.Formatter.format(self, record)}{self.NC}"


def setup_logger(name: str, level: int = logging.DEBUG, file_path: pathlib.Path = None) -> logging.Logger:
    """Create logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = ColorFormatter(fmt="%(message)s")

    # Don't add colors when logging to a file because they will not be displayed
    if file_path:
        file_handler = logging.FileHandler(f"{file_path}")
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def set_logging(file_path: pathlib.Path):
    """Set the default logger options."""
    logging.basicConfig(
        filename=f"{file_path}",
        level=WARNING,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )


def set_from_file(file_path: pathlib.Path):
    """"""
    with file_path.open("rt") as f:
        config_data = yaml.safe_load(f.read())
        logging.config.dictConfig(config_data)


def attach_wrapper(obj, func=None):  # Helper function that attaches function as attribute of an object
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def log(level: int, message: str) -> Callable:
    """Decorator to log."""
    def decorate(func: Callable) -> Callable:
        logger = logging.getLogger(func.__module__)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        log_message = f"{func.__name__} - {message}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, log_message)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)
        def set_level(new_level):
            nonlocal level
            level = new_level

        @attach_wrapper(wrapper)
        def set_message(new_message):
            nonlocal log_message
            log_message = f"{func.__name__} - {new_message}"

        return wrapper

    return decorate
