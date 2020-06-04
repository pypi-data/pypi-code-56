"""
injectify.api
~~~~~~~~~~~~~~~~~

This module contains the apis that power Injectify.
"""

from .injectors import BaseInjector


def inject(target: object, injector: BaseInjector):
    """Inject code in a target object."""
    def decorator(f):
        injector.prepare(target=target, handler=f)
        injector.compile(injector.visit_target())
        return f
    return decorator
