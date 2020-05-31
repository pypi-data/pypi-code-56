import logging


def disable_logging(logger_names, level=logging.WARNING):
    if isinstance(logger_names, str):
        logging.getLogger(logger_names).setLevel(level)
    elif isinstance(logger_names, (tuple, list)):
        for name in logger_names:
            logging.getLogger(name).setLevel(level)
    else:
        raise TypeError(f"Expected logger_names to be str, tuple or list, got "
                        f"{type(logger_names)} instead")


class LoggerMixin:
    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)

    @property
    def logger_name(self):
        module_name = self.__module__
        if module_name == "__main__":
            import inspect
            module_name = os.path.splitext(os.path.basename(
                inspect.getfile(self.__class__)
            ))[0]
        return '{}.{}'.format(module_name, self.__class__.__name__)
