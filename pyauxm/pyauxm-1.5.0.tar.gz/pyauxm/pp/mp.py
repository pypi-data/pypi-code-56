# coding: utf8
"""
Additions related to the `multiprocessing` module.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import functools
import contextlib
import multiprocessing
import multiprocessing.pool


@contextlib.contextmanager
def wrap_pool_map_args_over_fork(func, iterable, pool_factory=None):
    """
    Given the arguments for `multiprocessing.pool.Pool.map` (or `imap`, or `imap_unordered`),
    produces a pool and new arguments that will avoid pickling the original
    arguments,
    but are only viable within the context manager and the returned pool.

    This is essentially a multiprocessing-wrapped way of doing `fork()` and
    returning the result over pickle and a pipe.

    Note: the pool has to be created in this context manager as well, because
    the multiprocessing pool does `fork()`ing on init.

    Warning: consumes `iterable` before starting.
    """
    if pool_factory is None:
        pool_factory = multiprocessing.Pool

    inputs = list(iterable)
    indices = list(range(len(inputs)))

    globals_container = wrap_pool_map_args_over_fork.state
    marker = repr(object())  # Or `str(uuid.uuid4())`
    container = dict(
        inputs=inputs,
        func=func,
    )
    globals_container[marker] = container
    pool = pool_factory()
    try:
        yield (
            pool,
            functools.partial(_wrap_pool_map_args_over_fork__process_one, marker),
            indices)
    finally:
        globals_container.pop(marker, None)
        pool.terminate()


wrap_pool_map_args_over_fork.state = {}


def _wrap_pool_map_args_over_fork__process_one(marker, idx):
    container = wrap_pool_map_args_over_fork.state[marker]
    return container['func'](container['inputs'][idx])
