"""
GMLP.game.animation
===================
"""
from __future__ import absolute_import

class Error(Exception):
    """Base Exception class for all custom exceptions"""
    pass


class InitializationError(Error):
    """Can't Continue With Function Because The Initialization Function Was Not Found"""


class Animate:
    def __init__(self, Surface, init=None, animation_function=None, *args, **kwargs):
        self.surface = Surface
        self.init = init
        self.anim_func = animation_function
        self.args = args
        self.kwargs = kwargs

        if self.init == None:
            raise InitializationError(
                """Can't Continue With Function Because The Initialization Function Was Not Found"""
            )
        else:
            pass
