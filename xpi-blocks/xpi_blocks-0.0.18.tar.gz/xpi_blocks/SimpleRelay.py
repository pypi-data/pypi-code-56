# **********************************************************************;
# * Project           : RPI_blocks
# *
# * Program name      : SimpleRelay.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200330
# *
# * Purpose           : Controlling SimpleRelay with GPIO
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202003    Viacheslav Karpizin      1      original version
# *

#
# Copyright (c) 2019, Viacheslav Karpizin, (c) 2016 Adafruit Industries, Tony DiCola
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
# **********************************************************************


import time
import RPi.GPIO as GPIO
import random


GPIO.setmode(GPIO.BOARD)


class SimpleRelay:

    def __init__(self, pin, defaultValue=False, reverse=False):
        self._pin = pin
        self._reverse = reverse

        GPIO.setup(self._pin, GPIO.OUT)
        if defaultValue == True:
            GPIO.output(self._pin, GPIO.HIGH)
        else:
            GPIO.output(self._pin, GPIO.LOW)

    def set(self, value):
        if value == True:
            GPIO.output(self._pin, GPIO.HIGH)
        else:
            GPIO.output(self._pin, GPIO.LOW)


def main():
    print "=========================================================="
    print "SimpleRelay demo for RPI series"
    print "=========================================================="
    time.sleep(2)

    relay = SimpleRelay(40, False, False)

    try:
        while True:
            time.sleep(5)
            relay.set(True)

            time.sleep(5)
            relay.set(False)

    except KeyboardInterrupt:
        # Ctrl-C to exit
        sys.exit(0)


if __name__ == "__main__":
    main()
