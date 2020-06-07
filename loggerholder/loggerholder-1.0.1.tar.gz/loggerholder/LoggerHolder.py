# -*- coding: utf-8 -*-
import sys
import os
import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler


class LoggerHolder(object):
    """
    静态类
    """
    LOGGER = None

    @classmethod
    def logger(cls):
        if cls.LOGGER is None:
            raise RuntimeError('Please call `hold` method before you call this method!')
        return cls.LOGGER

    @classmethod
    def holded(cls, args):
        cls.hold(args)
        return cls.LOGGER

    @classmethod
    def hold(cls, args):
        if args is None:
            cls.LOGGER = cls.createdefault()
            return cls

        if len(args) != 4 or len(args) != 5:
            raise RuntimeError('input args error!!!    %s' % args)

        filename, when, fmt, level = args[0], args[1], args[2], args[3]
        basedir = args[4] if len(args) == 5 else ''
        cls.LOGGER = cls.createlogger(filename, when, fmt, level, basedir=basedir)
        return cls

    @staticmethod
    def createdefault():
        return logging.getLogger('therootlogger')

    @staticmethod
    def createlogger(filename, when, fmt, level, basedir=''):
        """
        :param filename:
        'logs/webapp.log'           relative path
        '/path/to/logs/webapp.log'  absolute path
        :param when:
        'd'  by each day
        'h'  by each hour
        'w'  by each week
        :param fmt:
        '%(asctime)s %(process)d %(thread)d %(levelname)s: %(message)s'
        '%(asctime)s %(process)d %(thread)d %(levelname)s: %(message)s [in func %(funcName)s , %(pathname)s line %(lineno)d]'
        :param level:
        logging.DEBUG < logging.INFO < logging.WARN == logging.WARNING < logging.ERROR < logging.FATAL == logging.CRITICAL
        :param basedir:
        if the `filename` is relative path, then should define the `basedir`
        :return:
        """
        logger = logging.getLogger('therootlogger')

        if filename is not None:
            absfilename = filename if os.path.isabs(filename) else os.path.join(basedir, filename).replace('\\', '/')
            filehandler = TimedRotatingFileHandler(absfilename, when=when)
            filehandler.setFormatter(Formatter(fmt))
            filehandler.setLevel(level)
            logger.addHandler(filehandler)
        if True:
            consolehandler = StreamHandler(sys.stdout)
            consolehandler.setFormatter(Formatter(fmt))
            consolehandler.setLevel(level)
            logger.addHandler(consolehandler)

        logger.setLevel(level)
        return logger
