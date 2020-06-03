from async_mail.config import settings

import importlib


def get_backend(backend_path: str = ""):
    backend = backend_path or settings.EMAIL_BACKEND
    module_path, class_name = backend.rsplit('.', 1)
    module = importlib.import_module(module_path)
    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err

