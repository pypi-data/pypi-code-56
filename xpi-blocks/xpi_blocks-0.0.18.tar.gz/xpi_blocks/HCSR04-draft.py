
# **********************************************************************;
# * Project           : xPI.blocks
# *
# * Program name      : HCSR04.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20200417
# *
# * Purpose           : Handle with HC-SR04 ultrasonic distance sensor
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202004    Viacheslav Karpizin      1       original version
# *
#
# Copyright (c) 2019, Al Audet , 2020, Viacheslav Karpizin

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
# https://www.sparkfun.com/datasheets/Robotics/TB6612FNG.pdf
# **********************************************************************
import RPi.GPIO as GPIO
import time
import smbus_m
import sys
sys.path.append('./../')


GPIO.setmode(GPIO.BOARD)
# GPIO.setmode(GPIO.BCM)


class HCSR04:

	# Constructor
	def __init__(self, pin_transmit, pin_receive):

		self._trig = pin_transmit
		self._echo = pin_receive

		GPIO.setup(self._trig, GPIO.OUT)
		GPIO.setup(self._echo, GPIO.IN)

	def __del__(self):
		GPIO.cleanup()



    def __init__(
        self, trig_pin, echo_pin, temperature=20, unit="metric", gpio_mode=GPIO.BCM
    ):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin


    def raw_distance(self, sample_size=11, sample_wait=0.1):
        """Return an error corrected unrounded distance, in cm, of an object 
        adjusted for temperature in Celcius.  The distance calculated
        is the median value of a sample of `sample_size` readings.
        Speed of readings is a result of two variables.  The sample_size
        per reading and the sample_wait (interval between individual samples).
        Example: To use a sample size of 5 instead of 11 will increase the 
        speed of your reading but could increase variance in readings;
        value = sensor.Measurement(trig_pin, echo_pin)
        r = value.raw_distance(sample_size=5)
        Adjusting the interval between individual samples can also
        increase the speed of the reading.  Increasing the speed will also
        increase CPU usage.  Setting it too low will cause errors.  A default
        of sample_wait=0.1 is a good balance between speed and minimizing 
        CPU usage.  It is also a safe setting that should not cause errors.
        e.g.
        r = value.raw_distance(sample_wait=0.03)
        """

 

        speed_of_sound = 331.3 * math.sqrt(1 + (self.temperature / 273.15))
        sample = []
        # setup input/output pins
        GPIO.setwarnings(False)

        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        for distance_reading in range(sample_size):
            GPIO.output(self.trig_pin, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            echo_status_counter = 1
            while GPIO.input(self.echo_pin) == 0:
                if echo_status_counter < 1000:
                    sonar_signal_off = time.time()
                    echo_status_counter += 1
                else:
                    raise SystemError("Echo pulse was not received")
            while GPIO.input(self.echo_pin) == 1:
                sonar_signal_on = time.time()
            time_passed = sonar_signal_on - sonar_signal_off
            distance_cm = time_passed * ((speed_of_sound * 100) / 2)
            sample.append(distance_cm)
        sorted_sample = sorted(sample)
        # Only cleanup the pins used to prevent clobbering
        # any others in use by the program
        GPIO.cleanup((self.trig_pin, self.echo_pin))
        return sorted_sample[sample_size // 2]

    def depth(self, median_reading, hole_depth):
        """Calculate the depth of a liquid. hole_depth is the
        distance from the sensor to the bottom of the hole."""

        return hole_depth - median_reading

    def distance(self, median_reading):
        """Calculate the distance from the sensor to an object."""
        return median_reading



    @staticmethod
    def basic_distance(trig_pin, echo_pin, celsius=20):
        """Return an unformatted distance in cm's as read directly from
        RPi.GPIO."""

        speed_of_sound = 331.3 * math.sqrt(1 + (celsius / 273.15))
        GPIO.setup(trig_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        GPIO.output(trig_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        echo_status_counter = 1
        while GPIO.input(echo_pin) == 0:
            if echo_status_counter < 1000:
                sonar_signal_off = time.time()
                echo_status_counter += 1
            else:
                raise SystemError("Echo pulse was not received")
        while GPIO.input(echo_pin) == 1:
            sonar_signal_on = time.time()

        time_passed = sonar_signal_on - sonar_signal_off
        return time_passed * ((speed_of_sound * 100) / 2)






    
    
def main():
	print "=========================================================="
	print "HC-SR04 demo for xPI.blocks "
	print "=========================================================="
	time.sleep(0.5)
	
  test = HCSR04(pin1, pin2)

	try:
		while True:


			time.sleep(2)
			
	except KeyboardInterrupt:
		# Ctrl-C to exit
		sys.exit(0)


if __name__ =="__main__":
    main()   
    
