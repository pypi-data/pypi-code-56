"""This is the callbacks module of the expansion package. Contains Callback abstract base class and
predefined callback classes for use in expansion.ColoredPointHandler.simulate() or
expansion.ColoredPointHandler.run_callbacks.
"""

# pylint: disable=super-init-not-called, too-few-public-methods

__version__ = '1.0'
__author__ = 'Rajarshi Mandal'
__all__ = ['Callback',
           'Sample',
           'Print',
           'PygameGUI',
           'callback_from_function']

import abc
import os
import sys

import pygame as pg


class Callback(metaclass=abc.ABCMeta):
    """Abstract Base Class for all callbacks to derive from. """
    @abc.abstractmethod
    def __call__(self, epoch, handler):
        """Calls callback.

        Args:
            epoch (int): Current epoch number.
            handler (expansion.ColoredPointHandler): A :class:`expansion.ColoredPointHandler`
            instance on which the callback will operate on.
        """

class Sample(Callback):
    """Callback to save :attr:`expansion.ColoredPointHandler.arr` as an image file Names each
    image as the current epoch number.

    Args:
        directory (str): Directory in which to save the images.
        f_format (str): File format to save each image as,
            given as 'png' or 'jpg'.

    """
    def __init__(self, directory, f_format):
        self._directory = directory
        self._f_format = f_format

    def __call__(self, epoch, handler):
        handler.export_as_img().save((f'{self._directory}{os.path.sep}{epoch}.'
                                      f'{self._f_format.lower()}'))

class Print(Callback):
    """Callback to print the current epoch number and point count."""
    def __call__(self, epoch, handler):
        print(f'Epoch:  {epoch}, Point Count:    {len(handler.points)}')

class PygameGUI(Callback):
    """Callback to update a pygame GUI with :attr:`expansion.ColoredPoint.arr` Instantiates a Pygame
    window and clock. Sets window title as 'Expansion'.

    Args:
        length (int): Side length of square :attr:`expansion.ColoredPointHandler.arr`.
        dimensions (tuple(int)): Dimensions of pygame window.
        offset (:obj:`tuple(int)`, optional): Offset of :attr:`expansion.ColoredPointHandler.arr`
            on pygame window, given as (x, y). Defaults to no offset (0, 0).
        tick (:obj:`int`, optional): Tick to be passed to pygame.time.Clock.tick.
    """
    def __init__(self, length, dimensions, offset=(0, 0), tick=60): # pylint: disable=too-many-function-args
        self._offset = offset
        self._tick = tick
        self._window = pg.display.set_mode(dimensions)
        self._surface = pg.Surface((length, length))
        self._clock = pg.time.Clock()

        pg.display.set_caption('Expansion')

    def __call__(self, epoch, handler):
        arr = handler.export_as_arr()

        pg.surfarray.blit_array(self._surface, arr)
        self._window.blit(self._surface, self._offset)

        for event in pg.event.get():
            if event.type == pg.QUIT: # pylint: disable=no-member
                pg.quit() # pylint: disable=no-member
                sys.exit()

        pg.display.update()
        self._clock.tick(self._tick)

class _FunctionCallback(Callback):
    """Callback from a function. Use factory function
    :func:`expansion.callbacks.callback_from_function` instead of instantiating directly.

    Args:
        func (callable): Function to instantiate a callback from. Must have epoch and handler as
            keyword arguments, then keyword arguments that are fixed, before callback is called.
        **kwargs: Fixed keyword arguments to be passed to function, when callback is called.
    """
    def __init__(self, func, **kwargs):
        self._func = func
        self.__dict__.update(**kwargs)

    def __call__(self, epoch, handler):
        func = self._func
        del self._func
        func(epoch=epoch, handler=handler, **self.__dict__)
        self._func = func


def callback_from_function(func, **kwargs):
    """Instantiates a callback object from a function. Factory function for
    :class:`expansion.callbacks._FunctionCallback`.

    Args:
        func (callable): Function to instantiate a callback from. Must have epoch and handler as
            keyword arguments, then keyword arguments that are fixed, before callback is called.
        **kwargs: Fixed keyword arguments to be passed to function, when callback is called.

    Returns:
        expansion.callbacks._FunctionCallback: A :class:`expansion.callbacks._FunctionCallback`
            object
    """
    return _FunctionCallback(func, **kwargs)
