# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : L9110H.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20200330
# *
# * Purpose           : Control motor via L9110 driver
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
import RPi.GPIO as GPIO
import time
import sys
sys.path.append('./../')


GPIO.setmode(GPIO.BOARD)
# GPIO.setmode(GPIO.BCM)


class DRV8833:
	ain1 = ""
	ain2 = ""

	# Defaults
	freq = 200

	# Constructor

	def __init__(self, ain1, ain2):
		self.ain1 = ain1
		self.ain2 = ain2

		GPIO.setup(ain1, GPIO.OUT)
		GPIO.setup(ain2, GPIO.OUT)


    self.pa = GPIO.PWM(ain2, self.freq)

		self.pa.start(0)


# Speed from -100 to 100
	def drive(self,  speed ):
		# Negative speed for reverse, positive for forward
		# If necessary use reverse parameter in constructor
		dutyCycle = speed
		if(speed < 0):
			dutyCycle = dutyCycle * -1



      			if(speed > 0):
        			GPIO.output(self.ain1,GPIO.LOW)
        			self.pa.ChangeDutyCycle(dutyCycle)
      			else:
        			GPIO.output(self.ain1,GPIO.HIGH)
        			self.pa.ChangeDutyCycle(100-dutyCycle)



	def brake(self):

			self.pa.ChangeDutyCycle(0)
			GPIO.output(self.ain1,GPIO.LOW)



	def __del__(self):
		GPIO.cleanup()
    
    
    
 def main():
	print "=========================================================="
	print "L9110H demo for RPI Series "
	print "=========================================================="
	time.sleep(3)
	

  	test = L9110(15, 16)

	
	

	try:
		while True:

			      print(" forward, 100%")
      			test.drive(100) #Forward 100% dutycycle
      			time.sleep(3)


					
            print(" forward, 20%")
            test.drive(20) #Forward 100% dutycycle
            time.sleep(3)

      			print(" reverse, 100%")
      			test.drive(-100) #Backwards 100% dutycycle
      			time.sleep(3)

            print(" reverse, 10%")
            test.drive(-10) #Backwards 100% dutycycle
            time.sleep(3)


      
     	 		  print(" brake")
      			test.brake() #Short brake
      			time.sleep(1)


	except KeyboardInterrupt:
		# Ctrl-C to exit
		sys.exit(0)


if __name__ =="__main__":
    main()   
