from .core import Variable, Constant
from .functional import *
from .grad_fn import *
from .global_graph import *
from .initializers import *
from .objectives import MeanSquaredError, MeanAbsoluteError, SparseCrossEntropy, CrossEntropy, BinaryCrossEntropy, get_objective
from .optimizers import SGD, Momentum, RMSprop, AdaDelta, Adam, AdaGrad, get_optimizer

name = 'xshinnosuke-nn'
