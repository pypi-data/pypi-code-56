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


def button_callback(pin, state):
    print('{} Pin {} now at {}'.format(datetime.datetime.now(), pin, state))


def timed_button_callback(pin, duration):
    print('{} Pin {} now down for {}'.format(datetime.datetime.now(), pin, duration))


class TestPio(unittest.TestCase):
    def don_test_ColorLed(self):
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

    def test_led(self):
        print('Starting test_Led')
        led = pio.Led(26, False)
        while True:
            print('Turning on')
            led.turn_on()
            time.sleep(5)
            print('Turning off')
            led.turn_off()
            time.sleep(5)

    def dont_test_Button(self):
        print('Starting test_Button')
        pio.Button(16, button_callback)
        while True:
            time.sleep(1)

    def dont_test_TimedButton(self):
        print('Starting test_TimedButton')
        pio.Button(16, timed_button_callback())
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

    def test_ADC(self):
        adc = pio.ADC(gain=1, r1=1000000, r2=220000, tolerance=.1, update=.1)
        adc.start()
        time.sleep(1)
        while True:
            print('{time}\t{count}'.format(time=datetime.datetime.now(), count=i))
            while not pio.ADC.adc_queue.empty():
                values = pio.ADC.adc_queue.get()
                print('{time_stamp}\t{v0:.5f}\t{a0}\t{v1:.5f}\t{a1}\t{v2:.5f}\t{a2}\t{v3:.5f}\t{a3}'.format(
                    time_stamp=values.time_stamp,
                    v0=values.voltages[0], a0=values.values[0],
                    v1=values.voltages[1], a1=values.values[1],
                    v2=values.voltages[2], a2=values.values[2],
                    v3=values.voltages[3], a3=values.values[3]))
            time.sleep(1)
        pio.ADC.stop()


if __name__ == '__main__':
    if not pio.pio_loaded:
        print('PIO not loaded. Cannot proceed')
    unittest.main()
