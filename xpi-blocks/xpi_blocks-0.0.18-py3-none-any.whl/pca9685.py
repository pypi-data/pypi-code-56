# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : pca9685.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200121
# *
# * Purpose           : Manipulate servos and led with PWM
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 201910    Viacheslav Karpizin      1      original version
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
#
# **********************************************************************


from __future__ import division
import logging
import time
import math
import sys
import smbus_m


# Registers/etc:
PCA9685_ADDRESS = 0x40
MODE1 = 0x00
MODE2 = 0x01
SUBADR1 = 0x02
SUBADR2 = 0x03
SUBADR3 = 0x04
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09
ALL_LED_ON_L = 0xFA
ALL_LED_ON_H = 0xFB
ALL_LED_OFF_L = 0xFC
ALL_LED_OFF_H = 0xFD

# Bits:
RESTART = 0x80
SLEEP = 0x10
ALLCALL = 0x01
INVRT = 0x10
OUTDRV = 0x04


logger = logging.getLogger(__name__)


# def software_reset(i2c=None, **kwargs): #TODO fix for specifix addresses
#    """Sends a software reset (SWRST) command to all servo drivers on the bus."""
#    # Setup I2C interface for device 0x00 to talk to all of them.
#    if i2c is None:
#        import Adafruit_GPIO.I2C as I2C
#        i2c = I2C
#    self._device = i2c.get_i2c_device(0x00, **kwargs)
#    self._device.writeRaw8(0x06)  # SWRST


class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, address=PCA9685_ADDRESS, bus_id=0, **kwargs):
        """Initialize the PCA9685."""
        # Setup I2C interface for the device.
        self.bus_id = bus_id
        self.bus = smbus_m.SMBus3(bus_id)
        self.addr = address

        self.set_all_pwm(0, 0)
        self.bus.write_byte_data(self.addr, MODE2, OUTDRV)
        self.bus.write_byte_data(self.addr, MODE1, ALLCALL)
        time.sleep(0.005)  # wait for oscillator
        mode1 = self.bus.read_byte_data(self.addr, MODE1)
        print(mode1)
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        print(mode1)
        self.bus.write_byte_data(self.addr, MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        logger.debug('Setting PWM frequency to {0} Hz'.format(freq_hz))
        logger.debug('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        logger.debug('Final pre-scale: {0}'.format(prescale))
        oldmode = self.bus.read_byte_data(self.addr, MODE1)
        print(oldmode)
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        print(newmode)
        self.bus.write_byte_data(self.addr, MODE1, newmode)  # go to sleep
        self.bus.write_byte_data(self.addr, PRESCALE, prescale)
        self.bus.write_byte_data(self.addr, MODE1, oldmode)
        print(prescale)
        time.sleep(0.005)
        self.bus.write_byte_data(self.addr, MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        self.bus.write_byte_data(self.addr, LED0_ON_L+4*channel, on & 0xFF)
        self.bus.write_byte_data(self.addr, LED0_ON_H+4*channel, on >> 8)
        self.bus.write_byte_data(self.addr, LED0_OFF_L+4*channel, off & 0xFF)
        self.bus.write_byte_data(self.addr, LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        self.bus.write_byte_data(self.addr, ALL_LED_ON_L, on & 0xFF)
        self.bus.write_byte_data(self.addr, ALL_LED_ON_H, on >> 8)
        self.bus.write_byte_data(self.addr, ALL_LED_OFF_L, off & 0xFF)
        self.bus.write_byte_data(self.addr, ALL_LED_OFF_H, off >> 8)


def main():
    print "=========================================================="
    print "PCA9685 demo for RPI series"
    print "=========================================================="
    time.sleep(3)

    # logging.basicConfig(level=logging.DEBUG)

    # Initialise the PCA9685 using the default address (0x40).
    #pwm = Adafruit_PCA9685.PCA9685()

    # Alternatively specify a different address and/or bus:
    pwm = PCA9685(address=0x40, busnum=0)

    # Configure min and max servo pulse lengths
    servo_min = 150  # Min pulse length out of 4096
    servo_max = 600  # Max pulse length out of 4096

    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)

    print('Moving servo on channel 0, press Ctrl-C to quit...')
    while True:
        # Move servo on channel O between extremes.
        pwm.set_all_pwm(0, servo_min)
        time.sleep(1)
        pwm.set_all_pwm(0, servo_max)
        time.sleep(1)


if __name__ == "__main__":
    main()
