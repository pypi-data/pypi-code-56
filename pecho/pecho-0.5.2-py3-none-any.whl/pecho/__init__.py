# MIT License
#
# Copyright (c) 2019-2020 Nihaal Sangha
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

try:
    from importlib.metadata import version as _version
except ModuleNotFoundError:
    _version = lambda _: None

try:
    import colorama as _colorama
except ImportError:  # pragma: no cover
    _colorama = None
if _colorama is not None:
    _colorama.init()

try:
    from click import echo as _click_echo
except ImportError:  # pragma: no cover
    _click_echo = None

__all__ = ['echo', 'CLEAR_LINE']
__version__ = _version('pecho')

START_OF_LINE = '\r'
CLEAR_LINE = '\033[K'

_sentinel = object()


def echo(*objects, newline=False, newline_char='\n', end='', print_func=print, print_func_kwargs=_sentinel):
    if print_func_kwargs is _sentinel:
        print_func_kwargs = {}

    if objects:
        objects = (START_OF_LINE + CLEAR_LINE + str(objects[0]),) + objects[1:]
    else:
        objects = (START_OF_LINE + CLEAR_LINE,)

    if newline is True:
        end += newline_char

    if end:
        objects = objects[:-1] + (str(objects[-1]) + end,)

    if print_func == print:
        print_func_kwargs['end'] = ''
    elif print_func == _click_echo:
        # Can ignore `print_func is None` as print_func() will error
        print_func_kwargs['nl'] = False

    return print_func(*objects, **print_func_kwargs)
