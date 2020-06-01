import numpy as np
from typing import Callable, Any

np_log = np.log
np_log_10 = np.log10
np_log_1p = np.log1p
np_min = np.min
np_max = np.max
np_median = np.median
np_mean = np.mean
np_std = np.std
np_exp = np.exp
np_cos = np.cos
np_sin = np.sin
np_tan = np.tan
np_arcsin = np.arcsin
np_arccos = np.arccos
np_arctan = np.arctan
np_sinh = np.sinh
np_cosh = np.cosh
np_tanh = np.tanh
squared: Callable[[Any], Any] = lambda x: x ** 2
cube: Callable[[Any], Any] = lambda x: x ** 3