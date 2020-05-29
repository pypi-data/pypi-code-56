# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import ast
from . import common


class CheckerBase(object):
    version_info = common.VersionInfo()

    def __call__(self, ctx, tree):
        raise NotImplementedError()
