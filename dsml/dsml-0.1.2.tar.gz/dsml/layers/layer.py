from abc import abstractmethod
from abc import abstractproperty
from abc import ABC

class Layer(ABC):
    @abstractmethod
    def __passForward__():
        pass
    @abstractmethod
    def init():
        pass
    @abstractmethod
    def getWeights():
        pass
    @abstractmethod
    def getBiases():
        pass
