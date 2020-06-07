#!/usr/bin/env python
# coding: utf8
"""
...
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import time
import random
import multiprocessing.pool
from pyauxm.pp.mp import wrap_pool_map_args_over_fork


class UnpickleabilityError(Exception):
    """ Catcher-exception to imitate and unpickleable value """


class Unpickleable(object):
    """
    A container object that refuses to get pickled, raising UnpickleabilityError
    """

    def __init__(self, value):
        self.value = value

    def __getstate__(self):
        raise UnpickleabilityError(self)


def process_that_object(obj, do_sleep=True):
    """ Do whatever with an `Unpickleable` object. E.g. uncontainerize it. """
    if do_sleep:
        time.sleep(random.random())
    return obj.value


def main():
    objs = [Unpickleable(idx) for idx in range(100, 110)]

    pool_size = 3

    try:
        res = multiprocessing.pool.Pool(pool_size).map(process_that_object, objs)
    except UnpickleabilityError:
        pass  # expected
    else:
        raise Exception("Was supposed to raise", res)

    cm = wrap_pool_map_args_over_fork(
        process_that_object,
        objs,
        pool_factory=lambda: multiprocessing.pool.Pool(pool_size))
    with cm as (pool, func, args):
        res_ordered = list(pool.map(func, args))
        res_unordered = list(pool.imap_unordered(func, args))

    print(res_ordered)
    print(res_unordered)
    assert res_ordered == [process_that_object(obj, do_sleep=False) for obj in objs]


if __name__ == '__main__':
    main()
