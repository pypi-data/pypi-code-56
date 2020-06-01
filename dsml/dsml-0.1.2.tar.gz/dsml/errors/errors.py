from numpy import add
from numpy import subtract
from .error import Error
from numpy import mean

class MSE(Error):
    @staticmethod
    def __call__(x,y,gradient=False):
        if not gradient:
            return MSE.__getError__(x,y)
        return MSE.__getGradiant__(x,y)

    @staticmethod
    def __getError__(x,y):
        return mean(subtract(x,y)**2)
    @staticmethod
    def __getGradiant__(x,y):
        return 2*(subtract(x,y))
