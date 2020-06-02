#!/usr/bin/env python
#
# This file is part of zepl-device: https://gitlab.com/zepl1/zepl-device
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3.0-or-later

import os
import struct
import asyncio

from .runner import DummyRunner
from pprint import pprint

class DummyIo(DummyRunner):
    """Passthrough runner for zmq.PAIR via tcp between DummyDevice <-> DummyIo
    """
    def __init__(self, ctx, uri_dev_io, cfg):
        super(DummyIo, self).__init__(ctx, uri_dev_io, cfg)
