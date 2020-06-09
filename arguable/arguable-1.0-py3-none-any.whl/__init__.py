try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


__version__ = version(__name__)


from .base import Arguable
from .parser import FullHelpParser as ArgumentParser
