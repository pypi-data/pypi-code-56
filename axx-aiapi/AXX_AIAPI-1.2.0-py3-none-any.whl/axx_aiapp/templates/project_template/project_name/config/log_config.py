import datetime
import logging
import logging.config
import os
from logging.config import dictConfig

BASE_LOG_PATH = "/Users/yanchenning/Desktop/pythonLogs/{% project_name %}"

if not os.path.exists(BASE_LOG_PATH):
    os.makedirs(BASE_LOG_PATH)


class LogLevelFilter(logging.Filter):
    def __init__(self, pass_level):
        self.pass_level = pass_level

    def filter(self, record):
        print(record.levelno)
        if self.pass_level == record.levelno:
            return True
        return False


def config_log():
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            "gunicorn": {
                "level": "INFO",
                "handlers": ["info", "error", "warning"],
                "propagate": 1,
                "qualname": "gunicorn"
            },
            "console": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": 0,
                "qualname": "console"
            }
        },
        'filters': {
            'info_filter': {
                '()': "config.log_config.LogLevelFilter",
                "pass_level": logging.INFO
            },
            'error_filter': {
                '()': "config.log_config.LogLevelFilter",
                "pass_level": logging.ERROR
            },
            'warning_filter': {
                '()': "config.log_config.LogLevelFilter",
                "pass_level": logging.WARNING
            }
        },
        'handlers': {
            "info": {
                "class": 'concurrent_log.ConcurrentTimedRotatingFileHandler',
                'backupCount': 14,
                'when': 'midnight',
                'delay': False,
                'level': 'INFO',
                "formatter": "generic",
                "filters": ['info_filter'],
                "filename": os.path.join(BASE_LOG_PATH, 'info.log')
            },
            "error": {
                "class": 'concurrent_log.ConcurrentTimedRotatingFileHandler',
                'backupCount': 14,
                'when': 'midnight',
                'delay': False,
                'level': 'ERROR',
                "formatter": "generic",
                "filters": ['error_filter'],
                "filename": os.path.join(BASE_LOG_PATH, 'error.log')
            },
            "warning": {
                "class": 'concurrent_log.ConcurrentTimedRotatingFileHandler',
                'backupCount': 14,
                'when': 'midnight',
                'delay': False,
                'level': 'WARNING',
                "formatter": "generic",
                "filters": ['warning_filter'],
                "filename": os.path.join(BASE_LOG_PATH, 'warning.log')
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "console"
            }
        },
        'formatters': {
            "generic": {
                "format": "%(asctime)s [process=%(process)d] "
                          "[tx_id=] [level=%(levelname)s] "
                          "[timestamp="+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"] "
                          "[bu_id=JT_AILab] [app_id={% project_name %}] %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S]",
                "class": "logging.Formatter"
            },
            "console": {
                "format": "'[%(levelname)s][%(asctime)s] %(message)s'",
                "class": "logging.Formatter"
            }
        }
    })

