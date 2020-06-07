import functools, inspect
from .terminal import terminal
from typing import Callable


def _get_class_that_defined_method(meth: Callable) -> object:
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return None

# Decorator tools

class DecoratorTools(object):

    @staticmethod
    def log(*args, type='log') -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    to_log, cmd = logs, f"terminal.{type}(*logs)"
                    exec(cmd, globals(), locals())
                except AttributeError:
                    terminal.error(f"DecoratorTools.log: Tipo inválido de log utilizado na função {func.__name__}")
                except SyntaxError:
                    terminal.error(f"DecoratorTools.log: Tipo de log provavelmente não especificado na função {func.__name__}")
                response = func(*args, **kwargs)
                return response
            return wrapper
        if len(args) == 1 and callable(args[0]):
            logs = []
            return decorator(args[0])
        logs = args
        return decorator

    @staticmethod
    def count(*args) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                response = func(*args, **kwargs)
                terminal.count(name)
                return response
            return wrapper
        name = args[0]
        if len(args) == 1 and callable(args[0]):
            name = name.__name__
            return decorator(args[0])
        return decorator

    @staticmethod
    def stopwatch(*args, **kwargs) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> None:
                ti = time()
                response = func(*args, **kwargs)
                tf = time()
                terminal.warn(f"Tempo de execução de {func.__name__}: {(tf - ti) * multiply}")
                return response
            return wrapper
        if 'get_ms' in kwargs and type(kwargs['get_ms']) is bool:
            multiply = 1 if not kwargs['get_ms'] else 1000
        else:
            multiply = 1
        return decorator(args[0]) if len(args) == 1 and callable(args[0]) else decorator

    @staticmethod
    def override(*args, **kwargs) -> Callable:
        # Determina se uma exceção deve ser lançada ou se deve apenas imprimir um aviso no terminal
        stop_application = kwargs['get_error'] if 'get_error' in kwargs else False
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                def throw_error(msg: str, stop=False):
                    if stop:
                        raise Exception(msg)
                    else:
                        terminal.warn(msg)
                cls = _get_class_that_defined_method(func)
                parents = list(inspect.getmro(cls))
                # Remove object e a classe detentora do método de sua lista de parentes
                if cls in parents:
                    parents.remove(cls)
                if object in parents:
                    parents.remove(object)
                # Retorna erro se a classe não for herdada
                if len(parents) == 0:
                    error_msg = f"O método {func.__name__} não pode ser sobrescrito porque {cls.__name__} não é uma classe herdada"
                    throw_error(error_msg, stop_application)
                else:
                    # Verifica se o método existe em alguma classe-mãe
                    exists = next((True for parent in parents if func.__name__ in dir(parent)), False)
                    # Retorna erro se o método não existir em uma de suas classes-mãe
                    if not exists:
                        parents_list = ', '.join([parent.__name__ for parent in parents])
                        error_msg = f"O método {func.__name__}() da classe {cls.__name__} não está definido em sua(s) super classe(s) ({parents_list}) e por isso não foi sobrescrito"
                        throw_error(error_msg, stop_application)
                return func(*args, **kwargs)
            return wrapper
        return decorator(args[0]) if len(args) == 1 and callable(args[0]) else decorator
