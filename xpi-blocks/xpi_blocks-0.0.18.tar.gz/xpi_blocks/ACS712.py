
#!/usr/bin/env python


# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : ACS712.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200317
# *
# * Purpose           : Current measurement with ADS1115 + voltage divider
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202003    Viacheslav Karpizin      1      original version
# *
# ACS712 Model 	Optimized Current Range	 	Output Sensitivity
#
# ACS712 ELC-05		+/- 5A			185 mV/A
#
# ACS712 ELC-20		+/- 20A			100 mV/A
#
# ACS712 ELC-30		+/- 30A			66 mV/A
#
# Copyright (c) 2020, Viacheslav Karpizin
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
from ads1115 import ADS1115


# TODO: make a child of VoldDivider

class ACS712:

    def __init__(self, adcObject, channel, resUp, resDown, currentLimit=5):

        self._adc = adcObject
        self._channel = channel
        self._resUp = resUp
        self._resDown = resDown
        self._currentLimit = currentLimit

    def readAmps(self):
        value = self._adc.readAdc(self._channel)*4096/32768
        normValue = value - 1300
        voltValue = normValue * (self._resUp + self._resDown) / self._resDown
        print("volt = " + str(voltValue))
        if self._currentLimit == 5:
            mult = 0.185
        elif self._currentLimit == 20:
            mult = 0.100
        elif self._currentLimit == 30:
            mult = 0.066
        # else:
        #	;
            # TODO: raise exception
        ampValue = voltValue/mult
        return ampValue


def main():
    print("==========================================================")
    print("ACS712 current sensor  demo for RPI series")
    print("==========================================================")
    time.sleep(0.1)

    bus = 1
    addr = 0x48

    a = ADS1115(bus, addr)

    v = ACS712(a, 2, 1000, 1000)

    print("sensor initialized...")
    try:
        while True:
            s = "(Ctrl-C to exit) ADC Result: "
            val = v.readAmps()
            s += ": %05d" % val+" mA  "
            print(s)
            time.sleep(0.5)
    except KeyboardInterrupt:

        print("interruption")
        # Ctrl-C to exit
        sys.exit(0)


if __name__ == "__main__":
    main()
