__version__ = "1.0.0"
__name__ = "Perceptron"
from .perceptron import Perceptron
# Importing all the activation functions
from .functions.activationFunctions.softmax import SoftMax
from .functions.activationFunctions.relu import ReLU
from .functions.activationFunctions.sigmoid import Sigmoid
from .functions.activationFunctions.heaviside import Heaviside
from .functions.activationFunctions.indentity import Identity
from .functions.activationFunctions.leaky_relu import LeakyReLU
from .functions.activationFunctions.sgn import Sign
from .functions.activationFunctions.smooth_relu import SmoothReLU
from .functions.activationFunctions.tanh import Tanh
# Importing all the loss functions
from .functions.lossFunctions.cross_entropy import CrossEntropy
from .functions.lossFunctions.quadratic_loss import QuadraticLoss
from .functions.lossFunctions.mean_abs_error import MeanAbsErr