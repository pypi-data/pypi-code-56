from abc import abstractmethod
from abc import ABC

class Error(ABC):
    @abstractmethod
    def __getError__():
        pass
    @abstractmethod
    def __getGradiant__():
        pass
