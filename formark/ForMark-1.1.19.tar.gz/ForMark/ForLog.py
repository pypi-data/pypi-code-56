import os
from loguru import logger

from ForMark.singleton import Singleton

"""
日志
"""


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR=os.getcwd()
# log_file_path = os.path.join(BASE_DIR, 'log/bb.log')

class ForLog(Singleton):
    def __init__(self, log_file_path="/logs/mark"):
        logger.add(
            log_file_path,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            filter="",
            level="INFO",
            enqueue=True,  # 异步写入
            retention="3 days"  # 一段时间后会清空
        )

    @classmethod
    def logger_info(cls, *msg):
        logger.info(msg)

    @classmethod
    def show(cls, *msg):
        logger.info(msg)

    @classmethod
    def logger_error(cls, *msg):
        logger.error(msg)
