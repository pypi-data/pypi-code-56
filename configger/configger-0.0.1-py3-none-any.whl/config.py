import os
import importlib.util

from .constants import *

class Config(object):

    REQUIREDS = (REQUIRED_STRING, REQUIRED_BOOL, REQUIRED_INT, REQUIRED_FLOAT)
    OPTIONALS = (OPTIONAL_STRING, OPTIONAL_BOOL, OPTIONAL_INT, OPTIONAL_FLOAT)

    def __init__(self, definitions):

        file_path = os.environ.get('CONFIGGER_FILE_PATH')
        if file_path is not None:
            self.MODE = CONFIGGER_MODE_FILE
            try:
                spec = importlib.util.spec_from_file_location("local", file_path)
                self.local = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.local)
            except FileNotFoundError as e:
                self.local = None
                raise Exception("Couldnt find the configger file at %s" % file_path)
        else:
            self.MODE = os.environ.get('CONFIGGER_MODE', CONFIGGER_MODE_DEFAULT)

        self.default = definitions

    def __getattr__(self, name):

        default_value = getattr(self.default, name)

        if self.MODE == CONFIGGER_MODE_ENV:

            envar = os.environ.get(name)

            if envar is None:
                if default_value in self.REQUIREDS:
                    raise Exception("Configuration value %s missing. In env mode all configuration must be given in docker environment variables." % name)
                elif default_value in self.OPTIONALS:
                    return None
                else:
                    return default_value
            else:
                if default_value in (REQUIRED_BOOL, OPTIONAL_BOOL) or isinstance(default_value, bool):
                    if envar == "false":
                        return False
                    return bool(envar)
                elif default_value in (REQUIRED_INT, OPTIONAL_INT) or isinstance(default_value, int):
                    return int(envar)
                elif default_value in (REQUIRED_FLOAT, OPTIONAL_FLOAT) or isinstance(default_value, float):
                    return float(envar)
                elif isinstance(default_value, str):
                    return envar
                else:
                    raise AttributeError(name)

        elif self.MODE == CONFIGGER_MODE_FILE:

            # return local else the default
            if default_value in self.REQUIREDS:
                local_value = getattr(self.local, name, None)
                if local_value is not None:
                    return local_value
                else:
                    raise Exception("Configuration value %s missing. Create a python file with values and set CONFIGGER_FILE_PATH to its location" % name)
            elif default_value in self.OPTIONALS:
                if self.local is None:
                    return None
                else:
                    return getattr(self.local, name, None)
            else:
                if self.local is None:
                    return default_value
                else:
                    return getattr(self.local, name, default_value)

        elif self.MODE in (CONFIGGER_MODE_DEFAULT, CONFIGGER_MODE_TEST):

            # the default else fail
            if default_value in self.REQUIREDS:
                raise Exception("Configuration value %s missing. Your need to explicitly overide this in your test. ie config.%s = xxxxx" % (name, name))
            elif default_value in self.OPTIONALS:
                return None
            else:
                return default_value
        else:
            raise Exception("unknown config mode %s" % self.MODE)



