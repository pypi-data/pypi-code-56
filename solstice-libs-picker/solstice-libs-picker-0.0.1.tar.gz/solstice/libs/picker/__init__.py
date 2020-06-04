#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for solstice-libs-picker
"""

from __future__ import print_function, division, absolute_import

import os
import sys

import tpDcc as tp

import solstice


def get_scripts_path():
    """
    Returns path where Solstice picker scripts are located
    :return: str
    """

    from tpDcc.libs.python import path as path_utils

    from solstice.libs.picker import scripts

    return path_utils.clean_path(scripts.__path__[0])


def load_script(name):
    """
    Function that loads a given MEL script by its name
    :param name: str, name of the script to load
    """

    if not tp.is_maya():
        return

    import tpDcc.dccs.maya as maya

    scripts_path = get_scripts_path()
    if not scripts_path or not os.path.isdir(scripts_path):
        return False

    script_to_load = os.path.join(scripts_path, name)
    if not os.path.isfile(script_to_load):
        solstice.logger.error('ERROR: Impossible to load {} script'.format(name))
        return False

    try:
        solstice.logger.debug('Loading MEL script: {}'.format(name))
        maya.mel.eval('source "{}"'.format(script_to_load).replace('\\', '/'))
        solstice.logger.debug('MEL script {} loaded successfully!'.format(name))
    except Exception as exc:
        solstice.logger.error('ERROR: Impossible to evaluate {} script'.format(name))
        solstice.logger.error('-' * 100)
        solstice.logger.error(str(exc))

    return True


def load_vl_scripts():
    """
    Loads all vl picker scripts
    """

    if not tp.is_maya():
        solstice.logger.warning('vl picker scripts are only available for Maya!')
        return False

    scripts_path = get_scripts_path()
    if not scripts_path or not os.path.isdir(scripts_path):
        solstice.logger.error('Impossible to initialize picker related scripts!')
        return False

    if scripts_path not in sys.path:
        sys.path.append(scripts_path)

    solstice.logger.info('Loading pickers MEL scripts ...')

    load_script('vlRigIt_getModuleFromControl.mel')
    load_script('vlRigIt_getControlsFromModuleList.mel')
    load_script('vlRigIt_selectModuleControls.mel')
    load_script('vlRigIt_snap_ikFk.mel')
    load_script('vlRigIt_snapParent.mel')
    load_script('vlRigIt_snapParentAskSetKey.mel')
    load_script('vl_resetTransformations.mel')
    load_script('vl_resetAttributes.mel')
    load_script('vl_contextualMenuBuilder.mel')

    return True


def init():
    """
    Initializes module
    """

    load_vl_scripts()

    return True
