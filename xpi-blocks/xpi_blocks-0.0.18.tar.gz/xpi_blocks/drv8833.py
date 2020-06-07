# **********************************************************************;
# * Project           : RPILib
# *
# * Program name      : DRV8833.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20200314
# *
# * Purpose           : Control both channels of DRV8833 motor driver chip
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
    bin1 = ""
    bin2 = ""

    # Defaults
    freq = 200

    # Constructor

    def __init__(self, ain1, ain2, bin1=none, bin2=none):
        self.ain1 = ain1
        self.ain2 = ain2
        self.bin1 = bin1
        self.bin2 = bin2

        GPIO.setup(ain1, GPIO.OUT)
        GPIO.setup(ain2, GPIO.OUT)
        if bin1 != None:
             GPIO.setup(bin1, GPIO.OUT)
        if bin2 != None:
             GPIO.setup(bin2, GPIO.OUT)

        self.pa = GPIO.PWM(ain2, self.freq)
        self.pb = GPIO.PWM(bin2, self.freq)
        self.pb.start(0)
        self.pa.start(0)


# Speed from -100 to 100

    def drive(self,  speed, motor=1):
        # Negative speed for reverse, positive for forward
        # If necessary use reverse parameter in constructor
        dutyCycle = speed
        if(speed < 0):
            dutyCycle = dutyCycle * -1

        if motor == 1:
            if(speed > 0):
                GPIO.output(self.ain1, GPIO.LOW)
                self.pa.ChangeDutyCycle(dutyCycle)
            else:
                GPIO.output(self.ain1, GPIO.HIGH)
                self.pa.ChangeDutyCycle(100-dutyCycle)
        elif motor == 2 and self.bin1 != None:
            if(speed > 0):
                GPIO.output(self.ain2, GPIO.LOW)
                self.pb.ChangeDutyCycle(dutyCycle)
            else:
                GPIO.output(self.ain2, GPIO.HIGH)
                self.pb.ChangeDutyCycle(100-dutyCycle)
        else:
                print("incorrect motor id")

    def brake(self, motor=1):
        if motor == 1:
            self.pa.ChangeDutyCycle(0)
            GPIO.output(self.ain1, GPIO.LOW)
        else:
            self.pb.ChangeDutyCycle(0)
            GPIO.output(self.bin1, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()



    def main():
        print("==========================================================")
        print("DRV8833 for RPI Series ")
        print("==========================================================")
        time.sleep(0.5)
	
        # test = DRV8833 (a1, a2, b1, b2, standby, reverse)
        test = DRV8833(15, 16,None, None, None, 11,False)

        try:
            while True:

                print("motor1, forward, 100%")
                test.drive(100) #Forward 100% dutycycle
                time.sleep(3)
					
                print("motor1, forward, 20%")
                test.drive(20) #Forward 100% dutycycle
                time.sleep(3)

                print("motor1, reverse, 100%")
                test.drive(-100) #Backwards 100% dutycycle
                time.sleep(3)

                print("motor1, reverse, 10%")
                test.drive(-10) #Backwards 100% dutycycle
                time.sleep(3)

                print("motor1, brake")
                test.brake() #Short brake
                time.sleep(1)

                print("motor1, standby")
 
                test.standby(True) #Enable standby
                test.standby(False) #Disable standby   
                time.sleep(2)
        except KeyboardInterrupt:
            # Ctrl-C to exit
            sys.exit(0)


if __name__ =="__main__":
    main()   
    
