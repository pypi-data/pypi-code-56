#!/usr/bin/env python


# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : VoltDiv.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200317
# *
# * Purpose           : Voltage measurement with ADS1115 + voltage divider
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202003    Viacheslav Karpizin      1      original version
# *

#
# Copyright (c) 2019, Viacheslav Karpizin, D. Scott Williamson
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
#
#
# **********************************************************************


# Imports
#
from __future__ import division
import time  # used for sleep function
import sys		# used for print function
import smbus  # I2Cimport spidev
from ads1115 import ADS1115


class VoltDiv:

    ################################################################################
    #
    # Variables
    #

    ################################################################################
    #
    # Functions
    #

    def __init__(self, adcObject, channel, resUp, resDown):

        self._adc = adcObject
        self._channel = channel
        self._resUp = resUp
        self._resDown = resDown

    def readVolt(self):
        value = self._adc.readAdc(self._channel)*4096/3300
        result = value * (self._resUp + self._resDown) / self._resDown
        return result/10000


def main():
    print "=========================================================="
    print "ADS1115 + voltage divider demo for RPI series"
    print "=========================================================="
    time.sleep(1)

    bus = 1
    addr = 0x48

    a = ADS1115(bus, addr)

    v = VoltDiv(a, 1, 30000, 1000)

    print("sensor initialized...")
    try:
        while True:
            s = "(Ctrl-C to exit) ADC Result: "
            val = v.readVolt()
            s += "Voltage: %05.3f" % val+" V  "
            print s
            time.sleep(0.5)
    except KeyboardInterrupt:

        print("interruption")
        # Ctrl-C to exit
        sys.exit(0)


if __name__ == "__main__":
    main()
