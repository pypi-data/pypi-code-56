# -*- coding: utf-8 -*-
# @Time: 2020/05/13
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:
import configparser
import logging
from logging import handlers
from aibase.common.project_path import log_cfg_path
UTF8 = 'utf-8'


# 日志输出到控制台，同时保存到文件
class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, config_path=None):
        # print(config_path)
        if config_path is None:
            config_path = log_cfg_path
        cf = configparser.RawConfigParser()
        cf.read(config_path, encoding=UTF8)
        format = cf.get('log', 'format')
        level = cf.get('log', 'level')
        output_type = cf.get('log', 'output_type')
        when = cf.get('log', 'when')
        filename = cf.get('log', 'filename')
        interval = cf.getint('log', 'interval')
        backup_count = cf.getint('log', 'backupCount')

        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(format)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别

        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, interval=interval,
                                               backupCount=backup_count,
                                               encoding=UTF8)  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式

        # 把对象加到logger里
        if output_type == 'console':
            self.logger.addHandler(sh)
        elif output_type == 'file':
            self.logger.addHandler(th)
        else:
            self.logger.addHandler(sh)
            self.logger.addHandler(th)


if __name__ == '__main__':
    log = Logger('../log_config.ini').logger
    test = 'test2'
    log.debug('debug')
    log.info('info%s' % test)
    log.warning('警告')
    log.error('报错')
    log.critical('严重')
