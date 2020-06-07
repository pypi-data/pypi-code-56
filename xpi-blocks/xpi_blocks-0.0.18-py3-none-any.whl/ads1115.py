#!/usr/bin/env python


# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : ads1115.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20191017
# *
# * Purpose           : Read data from 4-channel ADC
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 201910    Viacheslav Karpizin      1      original version
# *
# # ADS115 Datasheet can be found here:
# http://www.ti.com/lit/ds/symlink/ads1113.pdf
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
from __future__ import absolute_import
import time  # used for sleep function
import sys   # used for print function
#from . import smbus_m   # I2Cimport 
#from . import smbus_m
#import smbus_m
#import .smbus_m
#from .smbus_m import SMBus3
import smbus_m

class ADS1115:

    ################################################################################
    #
    # Variables
    #

    # get access to the SMBus (SMBus is a subset of the I2C protocol
    # 0 = /dev/i2c-0 (port I2C0)
    # 1 = /dev/i2c-1 (port I2C1) *this is the port on the GPIO's of RPi 3 B
    # bus = smbus_m.SMBus3(1)    # the 1 means use port I2C1

    # Address for the device

    # addr=0x48       # ADDR tied to GND
    # addr=0x49       # ADDR tied to VDD
    # addr=0x4A       # ADDR tied to SDA
    # addr=0x4B       # ADDR tied to SCL

    # Registers in the ADS1115
    DEVICE_REG_CONVERSION = 0x00
    DEVICE_REG_CONFIG = 0x01
    DEVICE_REG_LO_THRESH = 0x02
    DEVICE_REG_HI_THRESH = 0x03

    # Configuration register fields

    # Operational Status
    CONFIG_OS = 0X8000
    CONFIG_OS_START = 0X8000
    CONFIG_OS_PERFORMING_CONVERSION = 0X0000
    CONFIG_OS_NOT_PERFORMING_OPERATION = 0X8000

    # Differential measurements
    CONFIG_MUX_AIN0P_AIN1N = 0X0000  # (default)
    CONFIG_MUX_AIN1P_AIN3N = 0X1000
    CONFIG_MUX_AIN2P_AIN3N = 0X2000
    CONFIG_MUX_AIN3P_AIN3N = 0X3000
    #  Single ended measurements
    CONFIG_MUX_AIN0P_GNDN = 0X4000
    CONFIG_MUX_AIN1P_GNDN = 0X5000
    CONFIG_MUX_AIN2P_GNDN = 0X6000
    CONFIG_MUX_AIN3P_GNDN = 0X7000

    # Programmable gain amplifier configuration
    CONFIG_FSR_6V144 = 0X0000
    CONFIG_FSR_4V096 = 0X0200
    CONFIG_FSR_2V048 = 0X0400  # (default)
    CONFIG_FSR_1V024 = 0X0600
    CONFIG_FSR_0V512 = 0X0800
    CONFIG_FSR_0V256 = 0X0A00
    CONFIG_FSR_0V256 = 0X0C00
    CONFIG_FSR_0V256 = 0X0E00

    # Continuous or single shot mode
    CONFIG_MODE_CONTINUOUS = 0X0000
    CONFIG_MODE_SINGLE_SHOT = 0X0100  # (default)

    # Data rate
    CONFIG_DATA_RATE_8SPS = 0X0000
    CONFIG_DATA_RATE_16SPS = 0X0020
    CONFIG_DATA_RATE_32SPS = 0X0040
    CONFIG_DATA_RATE_64SPS = 0X0060
    CONFIG_DATA_RATE_128SPS = 0X0080  # (default)
    CONFIG_DATA_RATE_2508SPS = 0X00A0
    CONFIG_DATA_RATE_475SPS = 0X00C0
    CONFIG_DATA_RATE_860SPS = 0X00E0

    # Comparitor mode
    CONFIG_COMP_MODE_TRADITIONAL = 0X0000  # (default)
    CONFIG_COMP_MODE_WINDOW = 0X0010

    # Comparitor polarity
    CONFIG_COMP_POL_ACTIVE_LOW = 0X0000  # (default)
    CONFIG_COMP_POL_ACTIVE_HIGH = 0X0008

    # Comparitor latching
    CONFIG_COMP_LAT = 0X0004
    CONFIG_COMP_LAT_NON_LATCHING = 0X0000  # (default)
    CONFIG_COMP_LAT_LATCHING = 0X0004

    # comparitor queue and disable
    CONFIG_COMP_QUE = 0X0003
    CONFIG_COMP_QUE_1_CONV = 0X0000
    CONFIG_COMP_QUE_2_CONV = 0X0001
    CONFIG_COMP_QUE_4_CONV = 0X0002
    CONFIG_COMP_QUE_DISABLE = 0X0003  # (default)

################################################################################
#
# Functions

    def __init__(self, busid, addr,
                 voltage=CONFIG_FSR_4V096,
                 freq=CONFIG_DATA_RATE_128SPS):

        assert(addr == 0x48 or addr == 0x49 or addr == 0x4A or addr == 0x4B)
        assert(voltage == self.CONFIG_FSR_4V096
               or voltage == self.CONFIG_FSR_6V144
               or voltage == self.CONFIG_FSR_2V048
               or voltage == self.CONFIG_FSR_1V024)

        self._bus = smbus_m.SMBus3(busid)
        self._addr = addr
        self._voltage = voltage
        self._freq = freq

    def getVoltLimit(self):
        return self._voltage

    # swap endian of word (swap high and low bytes)
    # This is needed because the communication protocol uses a different byte
    # order than the Raspberry Pi
    def swap(self, a):
        return ((a & 0xff00) >> 8) | ((a & 0x00ff) << 8)

    # read ADC channel (blocking but quick)
    # all of the hardware access is in this function
    def readAdc(self, channel):
        #print("reading value...")
        # sanity check the channel specified
        if ((channel > 3) or (channel < 0)):
            return -1

        # Build read command
        config = (self.CONFIG_OS_START +				# start conversion
                  self.CONFIG_MUX_AIN0P_GNDN + 		# single ended conversion
                  (channel << 12) + 				# select channel
                  self._voltage + 				# 4.096v pre amp (3.3v signal)
                  self.CONFIG_MODE_SINGLE_SHOT + 		# single conversion and shutdown
                  self._freq + 		# data rate
                  self.CONFIG_COMP_MODE_TRADITIONAL + 	# comp conventional
                  self.CONFIG_COMP_POL_ACTIVE_LOW + 	# comp active low
                  self.CONFIG_COMP_LAT_NON_LATCHING + 	# comp non latching
                  self.CONFIG_COMP_QUE_DISABLE)		# comp disabled

        # Uncomment to see the config command in printed in hexadecimal
        # print 'config: %04X' % config

        # send read command (note byte swap)
        self._bus.write_word_data(
            self._addr, self.DEVICE_REG_CONFIG, self.swap(config))

        # wait for conversion to complete (blocking)
        while (True):
            # read status (note byte swap)
            status = self.swap(self._bus.read_word_data(
                self._addr, self.DEVICE_REG_CONFIG))

            # Uncomment to see the status printed in hexadecimal
            # print 'status: %04X' % status

            # when the Operational Status is no longer performing a conversion
            # we can break out of this wait loop
            if (status & self.CONFIG_OS) != self.CONFIG_OS_PERFORMING_CONVERSION:
                break

        # read result (note byte swap)
        result = self.swap(self._bus.read_word_data(
            self._addr, self.DEVICE_REG_CONVERSION))

        # return 16 bit integer A2D result for the specified channel
        return result


def main():
    print("==========================================================")
    print("ADS1115 demo for RPI series")
    print("==========================================================")
    time.sleep(1)

    bus = 0
    addr = 0x48

    a = ADS1115(bus, addr)

    print("sensor initialized...")
    try:
        while True:
            s = "(Ctrl-C to exit) ADC Result: "
            for i in range(0, 4):
                val = a.readAdc(i)
                s += str(i)+": %05d" % val+"  "
            print(s)
            time.sleep(0.5)
    except KeyboardInterrupt:

        print("interruption")
        # Ctrl-C to exit
        sys.exit(0)


if __name__ == "__main__":
    main()
