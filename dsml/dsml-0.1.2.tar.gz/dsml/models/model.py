from abc import *

class Model(ABC):
    @abstractmethod
    def predict():
        pass
    @abstractmethod
    def train():
        pass
    @abstractmethod
    def make():
        pass
