# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : mcp410xx.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20200306
# *
# * Purpose           : Read battery parameters from 3.7 lithium battery (used in UPS Lite module for RPI Zero)
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202003    Viacheslav Karpizin      1      original version
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

# load the spidev library
import spidev
import struct

# initialize spi
spi = spidev.SpiDev()


class MCP410xxPot:

         def __init__(self, bus=0, device=0):


                    # open the spi device
                spi.open(bus, device)
  spi.max_speed_hz = 500000

         def set_wiper(self, value = 0.5):
                """ Sets the wiper position

            input:
            -----

                value   : a value between 0 and 1 that sets the 
                          relative position of the potentiometer

            output:
            ------

                sends an SPI signal to the digipot to set the relative
                position of the wiper

        """

                # set the bounds of the value
                value = max([0, value])
                value = min([value, 1])

                # scale the value
                scaled_value = int(value * 255)

              # set the wiper write bit
                wiper_write = int(0b00010001)

                # send the wiper bit
                spi.xfer([wiper_write, scaled_value])


 
        def set_shutdown(self):
                """ Sets the total resistance

            input:
            -----

                value   : a value between 0 and 1 that sets the 
                          relative position of the potentiometer

            output:
            ------

                sends an SPI signal to the digipot to set the resistor network

        """

                # set the wiper write bit
                wiper_write = int(0b00100001)

                # send the wiper bit
                spi.xfer([wiper_write, 0])


if __name__ == "__main__":
            # get the wiper setting from the command line
        #import sys
        #val = float(sys.argv[1])

  print "=========================================================="
   print "MCP410xx demo for RPI series"
    print "Changing value from 0 to max value every 0.5 sec with 1/100 step"
    print "=========================================================="
    time.sleep(0.5)
        # test the wiper setting function
        mypot = MCP410xxPot()
        mypot.set_wiper(val)

  foreach i in (0..100):
       mypot.set_wiper(i/100)
        time.sleep(0.5)
