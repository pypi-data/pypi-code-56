import sklearn.utils.fixes
from numpy.ma import MaskedArray

# internal
from .wrappers import experiment_path


# version
__version__ = '0.0.2'

# fix skopt MaskedArray incompatibility
sklearn.utils.fixes.MaskedArray = MaskedArray
