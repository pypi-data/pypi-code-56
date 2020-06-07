

# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : x9cxxx.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200315
# *
# * Purpose           : Controlling digital potentiometer (x9c102, x9c103, x9c104, x9c503)
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
# https://www.renesas.com/eu/en/www/doc/datasheet/x9c102-103-104-503.pdf
# **********************************************************************


import time
import RPi.GPIO as GPIO
import random


GPIO.setmode(GPIO.BOARD)

#GPIO.setup(channel, GPIO.OUT)
# GPIO.input(channel)
#GPIO.output(channel, state)


DIGIPOT_UP = 1
DIGIPOT_DOWN = 0
DIGIPOT_MAX_AMOUNT = 99
DIGIPOT_UNKNOWN = 255


class X9Cxxx:

    def __init__(self, incPin, udPin, csPin):
        self._incPin = incPin
        self._udPin = udPin
        self._csPin = csPin
        self._currentValue = DIGIPOT_UNKNOWN

        GPIO.setup(self._incPin, GPIO.OUT)
        GPIO.setup(self._udPin, GPIO.OUT)
        GPIO.setup(self._csPin, GPIO.OUT)
        GPIO.output(self._csPin, GPIO.HIGH)

    def reset(self):
        print("inside reset")
        self.decrease(DIGIPOT_MAX_AMOUNT)
        self._currentValue = 0
        print(" currentValue = " + str(self._currentValue))

    def set(self, value):
        value = max(0, value)
        value = min(value, DIGIPOT_MAX_AMOUNT)

        if (self._currentValue == DIGIPOT_UNKNOWN):
            print("reset")
            self.reset()

        if (self._currentValue > value):
            self.change(DIGIPOT_DOWN, self._currentValue-value)
            print("going down for " + str(self._currentValue-value))
        elif (self._currentValue < value):
            self.change(DIGIPOT_UP, value-self._currentValue)
            print("going up for " + str(value-self._currentValue))

    def get(self):
        return _currentvalue

    def increase(self, amount):
        amount = max(0, amount)
        amount = min(amount, DIGIPOT_MAX_AMOUNT)
        self.change(DIGIPOT_UP, amount)

    def decrease(self, amount):
        print("inside decrease")
        amount = self.constrain(amount,  0, DIGIPOT_MAX_AMOUNT)
        self.change(DIGIPOT_DOWN, amount)

    def constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))

    def change(self, direction, amount):
        print("inside change")
        print("currentValue= " + str(self._currentValue))
        print("direction, amount " + str(direction) + " " + str(amount))

        amount = self.constrain(amount,  0, DIGIPOT_MAX_AMOUNT)

        GPIO.output(self._udPin, direction)
        GPIO.output(self._incPin, GPIO.HIGH)
        GPIO.output(self._csPin, GPIO.LOW)

        for i in range(0, amount):

            GPIO.output(self._incPin, GPIO.LOW)
            time.sleep(0.0002)

            GPIO.output(self._incPin, GPIO.HIGH)
            time.sleep(0.0002)
            if (self._currentValue != DIGIPOT_UNKNOWN):
                # _currentValue += (direction == DIGIPOT_UP ? 1 : -1)
                if direction == DIGIPOT_UP:
                    self._currentValue += 1
                else:
                    self._currentValue -= 1
                self._currentValue = self.constrain(
                    self._currentValue, 0, DIGIPOT_MAX_AMOUNT)

        GPIO.output(self._csPin, GPIO.HIGH)

        print(" (end) currentValue= " + str(self._currentValue))


def main():
    print "=========================================================="
    print "X9Cxxx demo for RPI series"
    print "=========================================================="
    time.sleep(2)

    #inc = 38
    #ud = 40
    #cs = 37

    pot = X9Cxxx(38, 40, 37)

    try:
        while True:
            value = 5  # = random.randint(0, 99)

            print("value = " + str(value))
            pot.set(value)

            time.sleep(5)

            value = 95  # = random.randint(0, 99)
            print("value = " + str(value))
            pot.set(value)

            time.sleep(5)

            value = 5  # = random.randint(0, 99)
            print("value = " + str(value))
            pot.set(value)

            time.sleep(5)

            value = 95  # = random.randint(0, 99)
            print("value = " + str(value))
            pot.set(value)

            time.sleep(5)

            value = 5  # = random.randint(0, 99)
            print("value = " + str(value))
            pot.set(value)

            time.sleep(5)

    except KeyboardInterrupt:
        # Ctrl-C to exit
        sys.exit(0)


if __name__ == "__main__":
    main()
