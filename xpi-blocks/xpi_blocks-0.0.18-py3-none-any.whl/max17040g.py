# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : max17040g.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20200117
# *
# * Purpose           : Read battery parameters from 3.7 lithium battery (used in UPS Lite module for RPI Zero)
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202001    Viacheslav Karpizin      1      original version
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
#
# **********************************************************************
import time
import smbus_m
import sys
sys.path.append('./../')


class MAX17040G:

    def __init__(self, bus_id, addr):
        """ Define connection
        Parameters:
        - addr: 0 = address pin is low; 1 = address pin is high.
        - bus:  The SMBus used. Rev 1 Pi uses 0; Rev 2 Pi uses 1.
        - mode: 0 to 5 = the mode as defined in the order above
        """
        self.bus_id = bus_id
        self.bus = smbus_m.SMBus3(self.bus_id)
        self.addr = addr

    def readVoltage(self):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        read = self.bus.read_word_data(self.addr, 2)
        swapped = (read >> 8) + ((read & 0xFF) << 8)
        voltage = swapped*1.25/1000/16
        return voltage

    def readCapacity(self):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        read = self.bus.read_word_data(self.addr, 4)
        swapped = (read >> 8) + ((read & 0xFF) << 8)
        capacity = swapped/256.0
        return capacity


def main():
    print "=========================================================="
    print "MAX17040G demo for RPI series"
    print "=========================================================="
    time.sleep(0.5)

    bus = 1

    address = 0x36        # MAX17040G
    sensor = MAX17040G(bus, address)

    try:
        while True:
            print("Capacity: %5.2f %", sensor.readCapacity())
            print("Voltage: %5.2f V", sensor.readVoltage())
            time.sleep(10)
    except KeyboardInterrupt:
        # Ctrl-C to exit
        sys.exit(0)


if __name__ == "__main__":
    main()
