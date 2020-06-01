import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from Common.Config import cfg as config


def get_log_level(level, def_value=None):
    if not isinstance(level, str):
        return def_value
    level = level.upper()
    return getattr(logging, level) if isinstance(getattr(logging, level), int) else def_value


log_level = logging.INFO
log_format = '%(asctime)s-%(levelname)s-%(module)s:%(lineno)d - %(message)s'
log_filemode = 'a'

logging_cfg = config.cfg.get('logging')
if isinstance(logging_cfg, dict):
    log_filemode = logging_cfg.get('filemode', log_filemode)
    if isinstance(logging_cfg.get('format'), str):
        log_format = logging_cfg.get('format').replace('&', '%')

    log_level = get_log_level(logging_cfg.get('level'), log_level)
    sentry_sdk_dsn = logging_cfg.get('sentry_sdk_dsn')
    if isinstance(sentry_sdk_dsn, str):
        if sentry_sdk_dsn.lower() != 'none':
            sentry_logging = LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=logging.ERROR  # Send errors as events
            )
            sentry_sdk.init(dsn=sentry_sdk_dsn, integrations=[sentry_logging])


def init_logger(log_filename=None):
    if log_filename is None:
        log_filename = logging_cfg.get('file')
    if isinstance(log_filename, str):
        log_filename = None if (log_filename.lower() == 'none' or log_filename.strip() == '') else log_filename
    logging.basicConfig(format=log_format, level=log_level)
    if log_filename is not None:
        file_handler = logging.FileHandler(log_filename, mode=log_filemode)
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(log_level)
        logging.getLogger().addHandler(file_handler)

