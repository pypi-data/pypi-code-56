import os
import sys
import tempfile

import sentry_sdk
from decouple import config
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

BASE_DIR = config(
    'BASE_DIR',
    default=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

STORAGE_DIR = config('STORAGE_DIR', default=os.path.join(BASE_DIR, 'storage'))
if not os.path.isdir(STORAGE_DIR):
    STORAGE_DIR = BASE_DIR

DATA_DIR = config('DATA_DIR', default=os.path.join(STORAGE_DIR, 'data'))
if not os.path.isdir(DATA_DIR):
    DATA_DIR = tempfile.gettempdir()

DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_ENGINE = config('DATABASE_ENGINE')
MIGRATED = config('MIGRATED', default=True, cast=bool)
TELNET_HOST = config('TELNET_HOST')
TELNET_PORT = config('TELNET_PORT')
TELNET_TIMEOUT = config('TELNET_TIMEOUT', default=300, cast=int)
TELNET_CONNECT_TIMEOUT = config('TELNET_CONNECT_TIMEOUT', default=60, cast=int)

TIMEZONE = config('TIMEZONE', default='Asia/Jakarta')

LOGGING_ROOT = config(
    'LOGGING_ROOT', default=os.path.join(STORAGE_DIR, 'logs'))
if not os.path.isdir(LOGGING_ROOT):
    LOGGING_ROOT = tempfile.gettempdir()

LOG_LEVEL = config('LOG_LEVEL', default='info').upper()

if DEBUG:
    LOG_LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{asctime} {levelname} {name} {process:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'production': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'tlr.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 7,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'production'],
            'level': LOG_LEVEL
        },
        '__main__': {
            'handlers': ['console', 'production'],
            'level': LOG_LEVEL,
            'propagate': False,
        }
    }
}

sentry_sdk.init(
    dsn=config('SENTRY_DSN', default=''),
    integrations=[SqlalchemyIntegration(), ]
)

LOCKFILE = os.path.join(DATA_DIR, 'tlr.lock')
