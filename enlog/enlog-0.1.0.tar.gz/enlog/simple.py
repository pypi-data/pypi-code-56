import logging
from typing import Optional, Union


def get_simple_logger(
        name: Optional[str] = None,
        console: bool = True,
        log_level: Optional[Union[str, int]] = logging.DEBUG,
        log_file: Optional[str] = None):
    """
    Create instance of logger.
    :param name: Logger name
    :param log_level: Log level
    :param log_file: Log file path
    :param console: Output to console if True
    :return: logging.Logger
    """
    if isinstance(log_level, str):
        log_level = logging.getLevelName(log_level)
    log_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    logger = logging.getLogger()
    if name is not None:
        logger.name = name
    logger.setLevel(log_level)
    if log_file:
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)
    return logger
