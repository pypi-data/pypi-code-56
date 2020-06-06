import unittest
from thompcoutils import pio as pio
import time
import datetime


#######################################
# Run like this in the parent folder:
# For all tests:
#   python -m unittest tests/test_pio.py 
# For only one test:
#   python -m unittest tests.test_pio.TestPio.test_ColorLed
#######################################

def motor_callback(is_running, event_time):
    if is_running:
        print("motor started at:{}".format(event_time))
    else:
        print("motor stopped at:{}".format(event_time))


def button_callback(pin, state, argument):
    print('{} Pin {} now at {}.  Message:{}'.format(datetime.datetime.now(), pin, state, argument))


def timed_button_callback(pin, duration, argument):
    print('{} Pin {} now down for {}.  Message;{}'.format(datetime.datetime.now(), pin, duration, argument))


class TestPio(unittest.TestCase):
    def dont_test_ColorLed(self):
        while True:
            print('Starting test_ColorLed')
            color_led = pio.ColorLed(23, 24, 25)
            print('RED')
            color_led.red()
            time.sleep(1)
            print('GREEN')
            color_led.green()
            time.sleep(1)
            print('BLUE')
            color_led.blue()
            time.sleep(1)
            print('CYAN')
            color_led.cyan()
            time.sleep(1)
            print('MAGENTA')
            color_led.magenta()
            time.sleep(1)
            print('WHITE')
            color_led.white()
            time.sleep(1)
            print('YELLOW')
            color_led.yellow()
            time.sleep(1)
            print('OFF')
            color_led.off()

    def dont_test_led(self):
        print('Starting test_Led')
        led = pio.Led(5, False)
        while True:
            print('Turning on')
            led.turn_on()
            time.sleep(1)
            print('Turning off')
            led.turn_off()
            time.sleep(1)

    def test_Button(self):
        import RPi.GPIO as GPIO
        print('Starting test_Button')
        while True:
            GPIO.remove_event_detect(16)
            pio.Button(pin=16, callback=button_callback)
        while True:
            time.sleep(1)

    def dont_test_TemperatureHumidity(self):
        temp_humid = pio.TemperatureHumidity(4, pio.TemperatureHumidity.SensorType.AM2302)
        temp_humid.start()
        while True:
            if temp_humid.queue.empty():
                print('waiting for sensor to stabilize')
            while not temp_humid.queue.empty():
                values = temp_humid.queue.get()
                print('{time}\tTemp:{temp:6.2f}°\tHumidity:{humid:6.1f}%'.format(time=values.time_stamp,
                                                                                 temp=values.temperature,
                                                                                 humid=values.humidity))
            time.sleep(1)

    def dont_test_TimedButton(self):
        print('Starting test_TimedButton')
        pio.TimedButton(16, timed_button_callback)
        while True:
            time.sleep(1)

    def dont_test_accelerometer(self):
        acc = pio.Accelerometer()
        static_motor_values = pio.Motor.get_resting_values(acc, 2000)
        motor = pio.Motor(acc, static_motor_values)
        motor.start(motor_callback)

        while True:
            print("motor is running:{}".format(motor.is_moving()))
            time.sleep(.5)

    def dont_test_ADC(self):
        adc = pio.ADC(gain=1, r1=1000000, r2=220000, tolerance=.1, update=.1)
        adc.start()
        time.sleep(1)
        while True:
            while not adc.queue.empty():
                values = adc.queue.get()
                if values.values[0]:
                    print('{time_stamp}\t'
                          'a0:{v0:6.4f}V\t{a0:-6d}\t'
                          'a1:{v1:6.4f}V\t{a1:-6d}\t'
                          'a3:{v2:6.4f}V\t{a2:-6d}\t'
                          'a3:{v3:6.4f}V\t{a3:-6d}'.format(time_stamp=values.time_stamp,
                                                           v0=values.voltages[0], a0=values.values[0],
                                                           v1=values.voltages[1], a1=values.values[1],
                                                           v2=values.voltages[2], a2=values.values[2],
                                                           v3=values.voltages[3], a3=values.values[3]))
            time.sleep(.1)


if __name__ == '__main__':
    if pio.pio_loaded:
        unittest.main()
    else:
        print('PIO not loaded. Cannot proceed')

