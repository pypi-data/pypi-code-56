# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : ShiftRegister74HC595.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200405
# *
# * Purpose           : Output shift register (serial to parallel)
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202004    Viacheslav Karpizin      1      original version
# *

#
# Copyright (c) 2020, Viacheslav Karpizin,
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


import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)


Class HC595():

    # Define MODES
    ALL = -1
    HIGH = 1
    LOW = 0

    # is used to store states of all pins
    _registers = list()

    # How many of the shift registers - you can change them with shiftRegisters method
    _number_of_shiftregisters = 1

       # ser_pin - serial, data in
       # rclk_pin - latch
       # srclk_pin - clock
       def __init__(self,  ser_pin, rclk_pin, srclk_pin, number_of_bits=8):

            custompins = 0
            self._serpin = SER_pin
            self._rclkpin = RCLK_pin
            self._srclkpin = SRCLK_pin
            self._number_of_bits = number_of_bits

            GPIO.setwarnings(True)

            GPIO.setup(self._serpin, GPIO.OUT)
            GPIO.setup(self._rclkpin, GPIO.OUT)
            GPIO.setup(self._srclkpin, GPIO.OUT)

        def startupMode(mode, execute= False):
            '''
            Allows the user to change the default state of the shift registers outputs
            '''
            if isinstance(mode, int):
                if mode is HIGH or mode is LOW:
                    _all(mode, execute)
                else:
                    raise ValueError(
                        "The mode can be only HIGH or LOW or Dictionary with specific pins and modes")
            elif isinstance(mode, dict):
                for pin, mode in mode.iteritems():
                    _setPin(pin, mode)
                if execute:
                    _execute()
            else:
                raise ValueError(
                    "The mode can be only HIGH or LOW or Dictionary with specific pins and modes")


        def digitalWrite(pin, mode):
            '''
            Allows the user to set the state of a pin on the shift register
            '''
            if pin == ALL:
                _all(mode)
            else:
                if len(_registers) == 0:
                    _all(LOW)

                _setPin(pin, mode)
            _execute()

        def delay(millis):
            '''
            Used for creating a delay between commands
            '''
            millis_to_seconds = float(millis)/1000
            return sleep(millis_to_seconds)

        def _all_pins():
            return _number_of_shiftregisters * 8

        def _all(mode, execute= True):

            #all_shr = _all_pins()

            for pin in range(0, self._number_of_bits):
                _setPin(pin, mode)
            if execute:
                _execute()

            return _registers

        def _setPin(pin, mode):
            try:
                _registers[pin] = mode
            except IndexError:
                _registers.insert(pin, mode)

        def _execute():
            #all_pins = _all_pins()
            GPIO.output(_RCLK_pin, GPIO.LOW)

            for pin in range(self._number_of_bits - 1, -1, -1):
                GPIO.output(_SRCLK_pin, GPIO.LOW)

                pin_mode = _registers[pin]

                GPIO.output(_SER_pin, pin_mode)
                GPIO.output(_SRCLK_pin, GPIO.HIGH)

            GPIO.output(_RCLK_pin, GPIO.HIGH)


def main():
    print "=========================================================="
    print "74HC595 shift register (serial in, parallel out) demo for RPI series"
    print "=========================================================="
    time.sleep(1)

    c = HC595(37, 38, 40)


    print("chip initialized...")
    try:
        while True:
            c.digitalWrite(1, GPIO.LOW)
            c.digitalWrite(2, GPIO.HIGH)


            time.sleep(0.5)
    except KeyboardInterrupt:

        print("interruption")
        # Ctrl-C to exit
        sys.exit(0)

if __name__ == "__main__":
    main()
