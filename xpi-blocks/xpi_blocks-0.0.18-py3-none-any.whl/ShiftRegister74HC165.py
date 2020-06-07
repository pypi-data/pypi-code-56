# DRAFT


# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : ShiftRegister74HC165.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200407
# *
# * Purpose           : Input Shift Register 74HC165 (parallel to serial)
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


import RPi.GPIO as io
import time


class ShiftReg():

    '''
    This class contains the code that on a low level handles interfacing with the register.
    It takes care of loading values into the register and reading the values out of the register
    '''

    def __init__(self, serial_out, load_pin, clock_enable, clock_pin, warnings=False, bitcount=8):
        '''
        :param serial_out: BCM GPIO pin that's connected to chip pin 9 (Serial Out)
        :param load_pin: BCM GPIO pin that's connected to chip pin 1 (PL, Shift/Load)
        :param clock_enable: BCM GPIO pin that's connected to chip pin 15 (Clock enable, Chip enable) not required
        :param clock_pin: BCM GPIO pin that's connected to chip pin 2 (Clock Pin
        :param warnings:
        :param bitcount: 8 for 1 chip, 16 for 2 chip one after another and so on
        '''

        io.setwarnings(warnings)
        io.setmode(io.BCM)
        self.data_pin = serial_out
        self.load_reg_pin = load_pin

        self.clock_pin = clock_pin
        self.clock_enable = clock_enable
        self._gpio_init()

        self.bitcount = bitcount

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.clean_gpio()

    def _gpio_init(self):
        '''Sets up GPIO pins for output and gives them their default value
        :return: Nothing
        '''

        # sets GPIO pins for output
        io.setup(self.data_pin, io.IN, pull_up_down=io.PULL_DOWN)
        io.setup(self.clock_pin, io.OUT)
        io.setup(self.clock_enable, io.OUT)
        io.setup(self.load_reg_pin, io.OUT)

        # sets default values on GPIO pins

        io.output(self.clock_pin, 0)
        io.output(self.clock_enable, 0)
        io.output(self.load_reg_pin, 1)

    def _read_input(self):
        '''This method will read the value on the serial out pin from the
        register
        :return: Value read from the register
        '''

        status = io.input(self.data_pin)

        return status

    def _cycle_clock(self, n=1):
        '''This method will cycle the clock pin high and low to shift
        the data down the register
        :param n: Number of times to cycle clock (Default 1 time)
        :return:
        '''

        self._shift_register(n)

    def _shift_register(self, n=1):
        ''' This method cycles the clock pin high and low which
        shifts the register down.
        :param n: number of times to cycle the clock pin (default 1 time)
        :return:
        '''

        for x in range(n):
            io.output(self.clock_pin, 1)
            io.output(self.clock_pin, 0)

        def read_input(self, bit):
            register = read_register()
            if bit < 0 or bit >= self.bitcount:
                raise IndexError
            value = register[bit]
            return value

    def read_register(self):
        '''This method handles reading the data out of the entire register.
        It loads the values into the register, shifts all of the values out of the
        register and reads the values storing them in a list left to right starting
        at Pin 0 going to the highest pin in your chain
        :return: List of pin values from the register lowest to highest pin.
        '''

        register = []

        # Loads the status of the input pins into the internal register
        self._load_register()

        # shifts out each bit and stores the value
        for x in range(self.bitcount):
            # Stores the value of the pin
            register.append(self._read_input())

            # Cycles the clock causing the register to shift
            self._shift_register()

        # reverses the list so it reads from left to right pin0 - pin7
        register.reverse()

        return register

    def _load_register(self):
        '''This method takes the values on the input pins of the register and loads
        them into the internal storage register in preperation to be shifted out of the
        serial port
        :return: Nothing
        '''

        io.output(self.load_reg_pin, 0)
        io.output(self.load_reg_pin, 1)

    def clean_gpio(self):
        '''This method cleans up the GPIO pins, it should be run whenever you are done
        interfacing with the GPIO pins like at the end of the script/program.
        :return:
        '''

        io.cleanup()


if __name__ == '__main__':

    '''
    This class serves as an example how to interface with the code above when trying to drop into a
    loop to read the input from a register. All we need to do is overwrite the handle_on_up and 
    handle_on_down methods and we can read input from our input register and dont have to worry
    about any low level handling.
    '''
    class Test(ReadHandler):
        def __init__(self, serial_out, load_pin, clock_enable, clock_pin, warnings=False, bitcount=8):
            ReadHandler.__init__(self, serial_out, load_pin,
                                 clock_enable, clock_pin, warnings, bitcount)

        def handle_on_up(self, pin):
            print('Pin {} has been changed to UP'.format(pin))

        def handle_on_down(self, pin):
            print('Pin {} has been changed to DOWN'.format(pin))

    with Test(26, 4, 6, 5) as t:
        try:
            t.watch_inputs()
        except KeyboardInterrupt:
            t.loop_breaker = True
            print('\nBroke Loop')
    '''
    t = ShiftReg(26, 4, 6, 5)
    while True:
        try:
            reg = t.read_register()
            print(reg, end='\r')
            time.sleep(.2)
        except KeyboardInterrupt:
            break
    t.clean_gpio()
    '''


def main():
    print "=========================================================="
    print "74HC165 shift register (parallel in, serial out) demo for RPI series"
    print "=========================================================="
    time.sleep(1)

    c = HC165(26, 4, 6, 5)

    print("chip initialized...")
    try:
        while True:

            reg = t.read_register()
            print(reg, end='\r')
            time.sleep(2)
    except KeyboardInterrupt:
        break

    t.clean_gpio()


if __name__ == "__main__":
    main()
