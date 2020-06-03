from abc import abstractmethod
from types import MethodType
from bingproxy.util import checkIfSubClass

class ProxyDecorator(object):
    def __init__(self, handlerClass):
        super().__init__()
        checkIfSubClass(handlerClass, InvocationHandler)
        self.__handlerClass = handlerClass
    
    def __call__(self, objClass):
        return Proxy(objClass, self.__handlerClass)

class Proxy(object):
    def __init__(self, objClass, handlerClass):
        super().__init__()
        self.__objClass = objClass
        self.__handlerClass = handlerClass

    def __call__(self, *args, **kwargs):
        return self

    def newInstance(self, *args, **kwargs):
        nestedObj = self.__objClass(*args, **kwargs)
        return ProxyInstance(nestedObj, self.__handlerClass())
        
class ProxyInstance(object):
    def __init__(self, nestedObj, invocationHandler):
        super().__init__()
        self._nestedObj = nestedObj
        self._invocationHandler = invocationHandler
        self._methodHandlers = {}

    def __getattr__(self, attr):
        exists = hasattr(self._nestedObj, attr)
        res = None
        if exists:
            res = getattr(self._nestedObj, attr)
            if isinstance(res, MethodType):
                if self._methodHandlers.get(res) is None:
                    self._methodHandlers[res] = MethodHandler(self, self._nestedObj, res, self._invocationHandler)
                return self._methodHandlers[res]
            else:
                return res
        else:
            return res

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._nestedObj, name, value)

class MethodHandler(object):
    def __init__(self, proxy, nestedObj, func, invocationHandler):
        super().__init__()
        self._proxy = proxy
        self._nestedObj = nestedObj
        self._func = func
        self._invocationHandler = invocationHandler
        
    def __call__(self, *args, **kwargs):
        return self._invocationHandler.invoke(self._proxy, self._func, self._nestedObj, *args, **kwargs)
            
class InvocationHandler(object):
        
    def invoke(self, proxy, func, nestedObj, *args, **kwargs):
        return func(*args, **kwargs)
