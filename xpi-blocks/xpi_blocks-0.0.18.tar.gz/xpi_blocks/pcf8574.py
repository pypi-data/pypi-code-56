# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : pcf8574.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20191119
# *
# * Purpose           : Handle 8-channel I2C in/out multiplexer
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 201911    Viacheslav Karpizin      1      original version
# *
#
# Copyright (c) 2019, Viacheslav Karpizin
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


import smbus_m
import time
import sys

sys.path.append('./../')
sys.path.append('./')


class PCF8574:
    def __init__(self, bus_id, address):
        self.bus_no = bus_id
        self.bus = smbus_m.SMBus3(self.bus_no)
        self.address = address

    def write(self, pin, value):
        """
        Set a specific output high (True) or low (False).
        """
        assert pin in range(
            8), "Output number must be an integer between 0 and 7"
        current_state = self.bus.read_byte(self.address)
        bit = 1 << 7-pin
        new_state = current_state | bit if value else current_state & (
            ~bit & 0xff)
        self.bus.write_byte(self.address, new_state)

    def read(self, pin):
        """
        Get the boolean state of an individual pin.
        """
        assert pin in range(8), "Pin number must be an integer between 0 and 7"
        state = self.bus.read_byte(self.address)
        return bool(state & 1 << 7-pin_number)


def main():

    print "=========================================================="
    print "PCF8574 demo for RPI series"
    print "=========================================================="
    time.sleep(0.5)

    addr = 0x20

    bus = 1
    chip = PCF8574(bus, addr)

    while True:
        chip.write(0, 1)
        time.sleep(1)
        chip.write(1, 1)
        time.sleep(1)
        chip.write(2, 1)
        time.sleep(1)
        chip.write(3, 1)
        time.sleep(1)
        chip.write(4, 1)
        time.sleep(1)
        chip.write(5, 1)
        time.sleep(1)
        chip.write(6, 1)
        time.sleep(1)
        chip.write(7, 1)
        time.sleep(1)

        chip.write(0, 0)
        time.sleep(1)
        chip.write(1, 0)
        time.sleep(1)
        chip.write(2, 0)
        time.sleep(1)
        chip.write(3, 0)
        time.sleep(1)
        chip.write(4, 0)
        time.sleep(1)
        chip.write(5, 0)
        time.sleep(1)
        chip.write(6, 0)
        time.sleep(1)
        chip.write(7, 0)
        time.sleep(1)


if __name__ == "__main__":
    main()
