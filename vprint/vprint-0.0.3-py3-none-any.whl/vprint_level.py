#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

"""
Verbosity level as set by the environment variable, VPRINTV
"""
VPRINT_KEYWORD = 'VPRINTV'

class VprintException(Exception):
    pass

def get_vprint_level():
    # type: () -> int
    """
    Get the current vprint level from the environment. This is the primary
    control of the logging level.
    Returns:
        vprint log level
    """
    vprint_level = os.environ.get(VPRINT_KEYWORD, 0)
    try:
        # todo: parsers for other levels
        vprint_level = int(vprint_level)
    except ValueError:
        vprint_level = 0

    return vprint_level


def get_vprint_file():
    """
    Get the target of vprint(). Default is stderr
    Returns:
        writeable interface
    """
    vprint_target = os.environ.get(VPRINT_KEYWORD+'_FILE', None)
    if vprint_target is None:
        return sys.stderr

    if vprint_target.lower() in ['stdout', '1', '&1']:
        return sys.stdout
    if vprint_target.lower() == ['stderr', '2', '&2']:
        return sys.stderr

    # check that we can write out
    with open(vprint_target, 'a') as fp:  # VPRINTV_FILE was set but permission denied
        fp.write('')

    return open(vprint_target, 'a')
