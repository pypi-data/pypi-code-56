from .logger import init_logger


class BaseHelpers(object):
    def __init__(self, name=None, name_log=None, log_level='INFO', config=None, **kwargs):
        log = kwargs.get('log' or None)
        d = {
            10: 'DEBUG',
            20: 'INFO'
        }
        log_level = d[log.getEffectiveLevel()] if log is not None else log_level
        self.name = name or __name__
        self.log_level = log_level if log is None else log.getEffectiveLevel()
        self.name_log = name_log if name_log is not None else str(self.__class__.__name__)
        self.config = config if config is not None else dict()
        self.log = log.getChild(self.name_log) if log is not None else init_logger(self.name_log)
        self.log.setLevel(log_level.upper())
        self.debug = kwargs.get('debug', False)