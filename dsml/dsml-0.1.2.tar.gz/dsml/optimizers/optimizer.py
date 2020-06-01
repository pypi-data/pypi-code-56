from abc import *

class Optimizer(ABC):
    @abstractmethod
    def getGradiants():
        pass
