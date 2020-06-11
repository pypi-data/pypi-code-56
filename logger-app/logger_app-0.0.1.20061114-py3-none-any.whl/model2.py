# -*- coding: utf-8 -*-
# @Time     : 2020-02-06 15:34
# @Author   : binger
import json
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from funcy import project
import os


class JsonStyle(object):
    """自定义 json 格式数去规则 """
    TO_STR = lambda info: json.dumps(info, separators=(",", ":"), ensure_ascii=False)
    default_format = ('message',)
    asctime_format = 'asctime'
    asctime_search = 'asctime'

    def __init__(self, fmt):
        self._fmt = fmt or self.default_format

    def usesTime(self):
        return self.asctime_search in self._fmt

    def format(self, record):
        keys = set(filter(lambda key: getattr(record, key, False), ["exc_text", "stack_info"]))
        if keys:
            keys.update(self._fmt)
        else:
            keys = self._fmt
        a = project(record.__dict__, keys)
        s = JsonStyle.TO_STR(a)
        return s


# 添加 json 日志格式
logging._STYLES["json"] = (JsonStyle, '{"levelname": levelname, "message":message}')


class FormatterRule(logging.Formatter):  # 自定义格式化类
    """重新实现日志输出规则工厂"""
    CB_TAG_MAP = {}

    def __init__(self, fmt=None, datefmt=None, style='%', cb_tag_map=None):
        self._cb_tag_map = cb_tag_map or self.CB_TAG_MAP
        if style != "json":
            field = ' '.join(list(map(lambda s: '%({})-2s'.format(s), self._cb_tag_map.keys())))
            fmt = fmt or '%(asctime)s.%(msecs)03d:{} %(filename)-12s[%(lineno)4d] %(levelname)-6s %(message)s'.format(
                field)
        else:
            fmt = {"asctime", "msecs", "filename", "lineno", "levelname", "message"}
            fmt.update(self._cb_tag_map.keys())
        # datefmt = '%Y-%m-%d %H:%M:%S'
        self.__fmt_style = style
        super(FormatterRule, self).__init__(fmt, datefmt, style)

    def format(self, record):
        """每次生成日志时都会调用, 该方法主要用于设置自定义的日志信息
        :param record 日志信息"""
        for tag, cb in self._cb_tag_map.items():
            setattr(record, tag, cb())

        if self.__fmt_style != "json":
            return super().format(record)  # 执行父类的默认操作
        else:
            record.message = record.getMessage()
            if self.usesTime():
                record.asctime = self.formatTime(record, self.datefmt)

            if record.exc_info:
                # Cache the traceback text to avoid converting it multiple times
                # (it's constant anyway)
                if not record.exc_text:
                    record.exc_text = self.formatException(record.exc_info)
            if record.stack_info:
                record.stack_info = self.formatStack(record.stack_info)

            return self.formatMessage(record)


def register_formatter_tag_mapper(mapper):
    """注册日志输出格式标识"""
    FormatterRule.CB_TAG_MAP = mapper


def load_styles():
    """获取日志风格"""
    return list(logging._STYLES.keys())


class LoggerApp(object):
    def __index__(self, log_file, log_err_file=None, separate_error_level=None):
        self._log_file = log_file
        if not log_err_file:
            self._log_err_file = "_err".join(os.path.splitext(log_file))
        else:
            self._log_err_file = log_err_file

        self.separate_error_level = separate_error_level

    def set_time_rotating_handler(self, when='d', interval=1, backupCount=0, encoding=None, delay=False,
                                  utc=False,
                                  atTime=None):
        file_handler = TimedRotatingFileHandler(filename=self._log_file,
                                                when=when, interval=interval,
                                                backupCount=backupCount,
                                                encoding=encoding,
                                                delay=delay,
                                                atTime=atTime,
                                                utc=utc)

        file_error_handler = TimedRotatingFileHandler(filename=self._log_file,
                                                      when=when, interval=interval,
                                                      backupCount=backupCount,
                                                      encoding=encoding,
                                                      delay=delay,
                                                      atTime=atTime,
                                                      utc=utc)

