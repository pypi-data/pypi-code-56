#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 23/04/2020
           '''

from pathlib import Path

from pyboy import PyBoy

loc = str(Path.home()/'Data'/'GB'/'ROMs'/'pokemon_blue.gb')

pyboy = PyBoy(loc)
while not pyboy.tick():
  pass
