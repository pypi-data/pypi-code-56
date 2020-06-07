# **********************************************************************;
# * Project           : RPI_blocks
# *
# * Program name      : ULN2003StepperMotorUnipolar.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20200403
# *
# * Purpose           : Control Unipolar stepper motor with uln2003 darlington driver
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202004    Viacheslav Karpizin      1       original version
# *
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
# http://robocraft.ru/files/datasheet/28BYJ-48.pdf
# **********************************************************************
import RPi.GPIO as GPIO
import time
import smbus_m
import sys
sys.path.append('./../')


# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)


class ULN2003StepperUniPolar:

    CW = True
    CCW = False

    # int Steps = 0
    # boolean Direction = true# gre
    # unsigned long last_time
    # unsigned long currentMillis
    stepsLeft = 4095
    # long time

    _steps = 0

    def rotateHalfStep(self, steps, direction):
        self._setDirection(direction)
        for x in range(0, steps):

            if self._steps == 0:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.HIGH)
            elif self._steps == 1:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.HIGH)
                GPIO.output(self._pin4, GPIO.HIGH)
            elif self._steps == 2:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.HIGH)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 3:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.HIGH)
                GPIO.output(self._pin3, GPIO.HIGH)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 4:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.HIGH)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 5:
                GPIO.output(self._pin1, GPIO.HIGH)
                GPIO.output(self._pin2, GPIO.HIGH)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 6:
                GPIO.output(self._pin1, GPIO.HIGH)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 7:
                GPIO.output(self._pin1, GPIO.HIGH)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.HIGH)
            else:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)

            self.adjustSteps()

    def rotateFullStep(self, steps, direction):
        self._setDirection(direction)
        for x in range(0, steps):

            if self._steps == 0:
                GPIO.output(self._pin1, GPIO.HIGH)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.HIGH)
            elif self._steps == 1:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.HIGH)
                GPIO.output(self._pin4, GPIO.HIGH)
            elif self._steps == 2:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.HIGH)
                GPIO.output(self._pin3, GPIO.HIGH)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 3:
                GPIO.output(self._pin1, GPIO.HIGH)
                GPIO.output(self._pin2, GPIO.HIGH)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)
            else:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)

            self.adjustSteps(4)

    def rotateOnePhase(self, steps, direction):
        self._setDirection(direction)
        for x in range(0, steps):

            if self._steps == 0:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.HIGH)
            elif self._steps == 1:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.HIGH)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 2:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.HIGH)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)
            elif self._steps == 3:
                GPIO.output(self._pin1, GPIO.HIGH)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)
            else:
                GPIO.output(self._pin1, GPIO.LOW)
                GPIO.output(self._pin2, GPIO.LOW)
                GPIO.output(self._pin3, GPIO.LOW)
                GPIO.output(self._pin4, GPIO.LOW)

            self.adjustSteps(4)

    def adjustSteps(self, totalSteps=8):
        if self._direction == True:
            self._steps = self._steps+1
        if self._direction == False:
            self._steps = self._steps-1
        if self._steps > totalSteps-1:
            self._steps = 0
        if self._steps < 0:
            self._steps = totalSteps-1

    def _setDirection(self, direction):
        self._direction = direction

    # Constructor
    def __init__(self, pin1, pin2, pin3, pin4):
        self._pin1 = pin1
        self._pin2 = pin2
        self._pin3 = pin3
        self._pin4 = pin4
        GPIO.setup(self._pin1, GPIO.OUT)
        GPIO.setup(self._pin2, GPIO.OUT)
        GPIO.setup(self._pin3, GPIO.OUT)
        GPIO.setup(self._pin4, GPIO.OUT)

        GPIO.output(self._pin1, GPIO.LOW)
        GPIO.output(self._pin2, GPIO.LOW)
        GPIO.output(self._pin3, GPIO.LOW)
        GPIO.output(self._pin4, GPIO.LOW)

    # def rotate(self, direction, steps ):

    def __del__(self):
        GPIO.cleanup()


def main():
    print "=========================================================="
    print "Unipolar Stepper Motor Handling with ULN2003 for RPI Series "
    print "=========================================================="
    time.sleep(0.5)

    stepsLeft = 4095

    stepper = ULN2003StepperUniPolar(5, 6, 13, 19)

    direction = ULN2003StepperUniPolar.CW

    try:
        while True:
            print("==================================================== ")
            print("Half stepping ")
            while stepsLeft > 0:
                time.sleep(0.01)

                stepper.rotateHalfStep(1, direction)
                stepsLeft = stepsLeft-1

            print("Change direction... ")
            time.sleep(2)
            direction = not direction
            stepsLeft = 4095

            while stepsLeft > 0:
                time.sleep(0.01)

                stepper.rotateHalfStep(1, direction)
                stepsLeft = stepsLeft-1

            print("Change direction... ")
            time.sleep(2)
            direction = not direction
            stepsLeft = 4095

            print("==================================================== ")
            print("full stepping ")
            while stepsLeft > 0:
                time.sleep(0.01)

                stepper.rotateFullStep(1, direction)
                stepsLeft = stepsLeft-1

            print("Change direction... ")
            time.sleep(2)
            direction = not direction
            stepsLeft = 4095

            while stepsLeft > 0:
                time.sleep(0.01)

                stepper.rotateFullStep(1, direction)
                stepsLeft = stepsLeft-1

            print("Change direction... ")
            time.sleep(2)
            direction = not direction
            stepsLeft = 4095

            print("==================================================== ")
            print("one phase  ")
            while stepsLeft > 0:
                time.sleep(0.01)

                stepper.rotateOnePhase(1, direction)
                stepsLeft = stepsLeft-1

            print("Change direction... ")
            time.sleep(2)
            direction = not direction
            stepsLeft = 4095

            while stepsLeft > 0:
                time.sleep(0.01)

                stepper.rotateOnePhase(1, direction)
                stepsLeft = stepsLeft-1

            print("Change direction... ")
            time.sleep(2)
            direction = not direction
            stepsLeft = 4095
    except KeyboardInterrupt:
        # Ctrl-C to exit
        sys.exit(0)


if __name__ == "__main__":
    main()
