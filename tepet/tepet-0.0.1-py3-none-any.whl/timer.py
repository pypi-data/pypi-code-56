"""
Module contains a single class. Some tricks applied, like disabling
garbage collection(it may affect execution time) and using a timing
function designed to performance-measurement use cases.
"""
import gc
import time

__all__ = ['Timer']


def _readable_time():
    return time.strftime('%Y %b %d %H:%M:%S +0000',
                         time.gmtime(time.time()))


def _printer(stuff):
    print(stuff)


class Timer:
    """
    This class can be used as both context manager and function decorator.
    It prints string with formatted time before executing targeted code, and
    follows with the message about time spent executing user's code.
    Examples:
    with Timer():
        ...

    or

    @Timer()
    def workload():
        ...

    Example output will be like:
    > 2020 May 31 19:36:30 +0000 ==== started
    > 2020 May 31 19:36:30 +0000 ==== elapses 0.00000 seconds
    """
    def __init__(self, scope=None):
        self.scope = scope or '===='
        self.gcold = None
        self.start = None

    def __enter__(self):
        self.gcold = gc.isenabled()
        gc.disable()
        time_readable = _readable_time()
        _printer('{time_readable} {scope} started'.format(
            time_readable=time_readable, scope=self.scope))
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        if self.gcold:
            gc.enable()
        time_readable = _readable_time()
        result_time = end - self.start
        _printer(
            '{time_readable} {scope} elapsed {result_time:.5f} seconds'.format(
                time_readable=time_readable, scope=self.scope,
                result_time=result_time
            ))

    def __call__(self, func):
        def callback(*args, **kwargs):
            with self:
                func(*args, **kwargs)

        return callback
