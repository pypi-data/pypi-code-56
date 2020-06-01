# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 8:36
# @Author  : Desire
# @Email   : yangyin1106@163.com
# @Blog    : https://www.cnblogs.com/desireyang/
# @File    : Logging_Handle
# @Software: PyCharm
# Explain  : 处理日志
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler



class MyLog(object):
    """封装的日志类"""

    def __init__(
            self,
            log_name='',
            level='DEBUG',
            sh_level='DEBUG',
            fh_level='DEBUG'):
        """
        初始化日志类
        :param log_name: 日志收集器名称
        :param level: 收集器等级
        :param sh_level: 输出到控制台等级
        :param fh_level: 输出到文件中的等级
        """
        self.level = level
        self.sh_level = sh_level
        self.fh_level = fh_level
        # 创建日志收集器
        self.my_log = logging.getLogger(log_name)
        # 设置日志收集器等级
        self.my_log.setLevel(level)

    def output(self, file_name='log.log', channel=0):
        """

        :param file_name:
        :param channel: 输出渠道，0：不进行轮转，1：按时间进行轮转，2：按大小进行轮转
        :return:
        """
        # 日志收集格式
        # formatter = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        formatter = '%(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(levelname)s - %(message)s'
        fmt = logging.Formatter(formatter)

        # 1、创建一个输出到控制台的输出渠道
        sh = logging.StreamHandler()
        # 2、设置输出等级
        sh.setLevel(self.sh_level)
        # 3、将输出渠道绑定到日志收集器上
        self.my_log.addHandler(sh)
        sh.setFormatter(fmt)

        channels = {
            0: logging.FileHandler,
            1: self.__channel_time,
            2: self.__channel_size,
        }

        fh = channels[channel](file_name, encoding='utf8')
        fh.setLevel(self.fh_level)
        self.my_log.addHandler(fh)

        fh.setFormatter(fmt)
        return self.my_log

    def __channel_time(self, file_name, encoding):
        """
        创建一个按时间轮转的文件输出渠道
        :param file_name:
        :return:
        """
        # 创建一个按时间轮转的文件输出渠道
        # interval: 设置时间间隔
        # when: 设置间隔单位（默认H）
        #      S-Seconds(秒)
        #      M-Minutes(分钟)
        #      H-Hours(小时)
        #      D-Days(天)
        # backupCount:轮转的文件数量
        fh = TimedRotatingFileHandler(filename=file_name,
                                      encoding=encoding,
                                      when='D',
                                      interval=1,
                                      backupCount=7)
        return fh

    def __channel_size(self, file_name, encoding):
        """
        创建一个按文件大小轮转过的文件输出渠道
        :param file_name:
        :return:
        """
        # 创建一个按文件大小轮转过的文件输出渠道
        # maxBytes: 设置文件的大小（单位：字节）
        #          1024个字节=1kb
        #          1024kb = 1Mb
        # backupCount: 轮转的文件数量
        fh = RotatingFileHandler(filename=file_name,
                                 mode='a',
                                 encoding=encoding,
                                 maxBytes=1024 * 1024 * 20,
                                 backupCount=3)
        return fh
