# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : VNH2SP30.py
# *
# * Author            : Viacheslav Karpizin,
# *
# * Date created      : 20200315
# *
# * Purpose           : Controlling powerful motor driver VNH2SP30
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


DIGIPOT_UP = 1
DIGIPOT_DOWN = 0
DIGIPOT_MAX_AMOUNT = 99
DIGIPOT_UNKNOWN = 255


class VNH2SP30:

  ina = ""
	inb = ""
	pwm = ""

	# Defaults
	freq = 200

	  def __init__(self, pwm, ina, inb):
      self._pwm = pwm
      self._ina = ina
      self._inb = inb  



      GPIO.setup(self._pwm, GPIO.OUT)		
      GPIO.setup(self._ina, GPIO.OUT)		
      GPIO.setup(self._inb, GPIO.OUT)
      GPIO.output(self._ina, GPIO.HIGH)
      GPIO.output(self._inb, GPIO.HIGH)

      self.pa = GPIO.PWM(self._pwm, self.freq)

      self.pa.start(0)


	  def set(self, power):
      print("inside set")
      //power:-100 to 100
      if power > 100:
        power = 100
      elif power < -100:
        power = -100

      if abs(power) > 0:
              if power > 0:
                      GPIO.output(self._ina, GPIO.HIGH)
                      GPIO.output(self._inb, GPIO.LOW)
              else:
                      GPIO.output(self._ina, GPIO.LOW)
                      GPIO.output(self._inb, GPIO.HIGH)

      else:
                      GPIO.output(self._ina, GPIO.HIGH)
                      GPIO.output(self._inb, GPIO.HIGH)


      self.pa.start(abs(power)/100)


	








def main():
	print "=========================================================="
	print "VNH2SP30 demo for RPI series"
	print "=========================================================="
	time.sleep(2)

	# pwm = 40
	# ina = 38
	# inb = 37


	motor = VNH2SP30(40, 38, 37)



	try:
		while True:
                for  i in range(-100, 100):
                        motor.turnMotor(i)
                        time.sleep(0.01)
                for  i in range(100, -100):
                        motor.turnMotor(i)
                        time.sleep(0.01)
			


			time.sleep(5)			


	except KeyboardInterrupt:
		# Ctrl-C to exit
		sys.exit(0)


if __name__ =="__main__":
    main()
