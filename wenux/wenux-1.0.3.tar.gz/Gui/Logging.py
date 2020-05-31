import sys
from PyQt5 import QtCore
import logging

def set_logging(debug):
    """Setup of run wide logging options

    :param debug is a bool value of debug argument

    Level of logging is setup based on the argument and logger is created
    with basic config

   """
    level = (logging.INFO, logging.DEBUG)[debug]
    if logging:
        logging.getLogger().setLevel(level)
    else:
        logging.basicConfig(level=level,
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

class OutputWrapper(QtCore.QObject):
    """Output redirect class

    This class overrides the functionality of OutputWrapper to allow
    user to use logging module and output it to any Qt object that supports
    text input

   """
    outputWritten = QtCore.pyqtSignal(object, object)

    def __init__(self, parent=None, stdout=True):
        QtCore.QObject.__init__(self, parent)
        if stdout:
            self._stream = sys.stdout
            sys.stdout = self
        else:
            self._stream = sys.stderr
            sys.stderr = self
        self._stdout = stdout

    def write(self, text):
        self._stream.write(text)
        self.outputWritten.emit(text, self._stdout)

    def __getattr__(self, name):
        return getattr(self._stream, name)

    def __del__(self):
        try:
            if self._stdout:
                sys.stdout = self._stream
            else:
                sys.stderr = self._stream
        except AttributeError:
            pass
