import time
import datetime
from thompcoutils.log_utils import get_logger
import threading
import sys
from thompcoutils.threading_utils import WorkerThread, ThreadManager
import thompcoutils.units as units
from queue import Queue


# noinspection PyBroadException
try:
    import RPi.GPIO as GPIO
    import Adafruit_ADS1x15
    import Adafruit_DHT
    import smbus
    GPIO.setmode(GPIO.BCM)
    pio_loaded = True
    get_logger().debug('GPIO successfully loaded')
except Exception as e:
    get_logger().critical('GPIO NOT loaded: {}'.format(e))
    pio_loaded = False


class ADC:
    singleton = None

    class Values:
        def __init__(self, time_stamp, values, voltages):
            self.time_stamp = time_stamp
            self.values = values
            self.voltages = voltages

    def __init__(self, chip='ADS1115', gain=1, r1=1000000, r2=220000, tolerance=.1, update=.25):
        if ADC.singleton is not None:
            raise RuntimeError('cannot create more than one ADC')
        self.gains = {1: 4.096, 2: 6.144, 3: 6.144, 4: 1.024, 8: 0.512, 16: 0.256}
        self.gain = gain
        self.r1 = r1
        self.r2 = r2
        self.tolerance = tolerance
        self.update = update

        self.queue = Queue(1000)
        self.last_voltage = [0] * 4

        # Create an ADS1115 ADC (16-bit) instance.
        if chip == 'ADS1115':
            self.adc = Adafruit_ADS1x15.ADS1115()
            self.resolution_range = {min: -32768, max: 32767}
        elif chip == 'ADS1015':
            self.adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
            self.resolution_range = {min: -2048, max: 2047}
        else:
            raise RuntimeError("Chip not selected")
        self.multiplier = 2 * self.gains[gain] / (self.resolution_range[max] - self.resolution_range[min])
        self.worker_thread = WorkerThread(callback_function=ADC._adc_thread, sleep=self.update, parameters=self)

    def stop(self):
        self.worker_thread.stop()

    @staticmethod
    def _adc_thread(adc):
        values = [0] * 4
        voltages = [0] * 4
        append = False
        time_stamp = datetime.datetime.now()
        for i in range(4):
            values[i] = adc.adc.read_adc(i, gain=adc.gain)
            v2 = values[i] * adc.multiplier
            v3 = ((adc.r1 * v2) / adc.r2) + v2
            voltages[i] = v3
            if v3 > adc.last_voltage[i] + adc.tolerance or v3 < adc.last_voltage[i] - adc.tolerance:
                append = True
            adc.last_voltage[i] = v3
        if append:
            adc.queue.put_nowait(adc.Values(adc, time_stamp, values, voltages))

    def start(self):
        ADC.running = True
        self.worker_thread.start()


class Button:
    # check out this article on debouncing:
    # https://www.raspberrypi.org/forums/viewtopic.php?t=134394
    def __init__(self, pin, callback, pull_up_down=GPIO.PUD_UP, package=None):
        self.pin = pin
        self.package = package
        self.last_push = datetime.datetime.now()
        self.callback = callback
        GPIO.setup(pin, GPIO.IN, pull_up_down=pull_up_down)
        GPIO.add_event_detect(pin, edge=GPIO.BOTH, callback=self._debounce_function)

    def _debounce_function(self, pin):
        time_now = datetime.datetime.now()
        current_state = GPIO.input(self.pin)
        if (time_now - self.last_push).microseconds > .1 * units.microseconds_per_second:
            self.callback(pin, current_state, self.package)
        self.last_push = time_now


class TimedButton:
    def __init__(self, pin, callback, pull_up_down=GPIO.PUD_UP, package=None):
        self.pin = pin
        self.package = package
        self.last_push = datetime.datetime.now()
        self.callback = callback
        self.press_time = None
        GPIO.setup(pin, GPIO.IN, pull_up_down=pull_up_down)
        GPIO.add_event_detect(pin, edge=GPIO.BOTH, callback=self._debounce_function)

    def _debounce_function(self, pin):
        time_now = datetime.datetime.now()
        current_state = GPIO.input(self.pin)
        if (time_now - self.last_push).microseconds > .1 * units.microseconds_per_second:
            if current_state:
                self.press_time = datetime.datetime.now()
            else:
                self.callback(pin, datetime.datetime.now() - self.press_time, self.package)
        self.last_push = time_now


class PiOut:
    def __init__(self, pin, initial_state=None):
        if pio_loaded:
            GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self.state = False
        if initial_state is not None:
            self.toggle(initial_state)

    def toggle(self, new_state=None):
        logger = get_logger()
        if new_state is None:
            self.state = not self.state
        else:
            self.state = new_state
        logger.debug("pin {} toggled {}".format(self.pin, self.state))
        if pio_loaded:
            GPIO.output(self.pin, self.state)

    def turn_on(self):
        GPIO.output(self.pin, True)

    def turn_off(self):
        GPIO.output(self.pin, False)


class Led(PiOut):
    def __init__(self, pin, initial_state=None):
        PiOut.__init__(self, pin, initial_state)


class FlashingLight(Led):
    def __init__(self, pin, time_on, time_off=None, count=None, initial_state=None):
        PiOut.__init__(self, pin, initial_state)
        self.time_on = time_on
        if time_off is None:
            self.time_off = time_on
        else:
            self.time_off = time_off
        self.count = count
        self.thread = None
        self.stopping = False

    def _flasher(self):
        logger = get_logger()
        self.toggle(True)
        logger.debug("FlashingLight pin {} is {}".format(self.pin, self.state))
        time.sleep(self.time_on)
        if self.thread.is_running:
            self.toggle(False)
        logger.debug("FlashingLight pin {} is {}".format(self.pin, self.state))
        time.sleep(self.time_off)
        if self.stopping and not self.state:
            self.thread.stop()

    def start(self):
        self.thread = WorkerThread(callback_function=self._flasher, sleep=.01)
        self.thread.start()

    def stop(self):
        self.stopping = True


class ColorLed:
    def __init__(self, red_pin, green_pin, blue_pin):
        self._red = Led(red_pin)
        self._green = Led(green_pin)
        self._blue = Led(blue_pin)
        self.off()

    def set_colors(self, red, green, blue):
        self._red.toggle(red)
        self._green.toggle(green)
        self._blue.toggle(blue)

    def red(self):
        self.set_colors(False, True, True)

    def green(self):
        self.set_colors(True, False, True)

    def blue(self):
        self.set_colors(True, True, False)

    def yellow(self):  # red & green
        self.set_colors(False, False, True)

    def magenta(self):  # red & blue
        self.set_colors(False, True, False)

    def cyan(self):  # blue & green
        self.set_colors(True, False, False)

    def white(self):  # red & green & blue
        self.set_colors(False, False, False)

    def off(self):
        self.set_colors(True, True, True)


class StateLight:
    class State:
        def __init__(self, light, duration):
            self.light = light
            self.duration = duration

    def __init__(self, state_list):
        self.state_list = state_list
        self.thread = None
        self.state = 0

    def _state_stepper(self):
        # activate the state
        state = self.state_list[self.state]
        if isinstance(state.light, FlashingLight):
            state.light.start()
        elif isinstance(state.light, Led):
            state.light.toggle(True)
        time.sleep(state.duration)
        # advance the counter
        if self.state >= len(self.state_list) - 1:
            self.state = 0
        else:
            self.state += 1
        # turn off the state
        if isinstance(state.light, FlashingLight):
            state.light.stop()
            while state.light.state:
                time.sleep(.01)
        elif isinstance(state.light, Led):
            state.light.toggle(new_state=False)

    def start(self):
        self.thread = WorkerThread(self._state_stepper)
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.thread.stop()
        for state in self.state_list:
            if isinstance(state.light, FlashingLight):
                state.light.stop()
            elif isinstance(state.light, Led):
                state.light.toggle(new_state=False)

    def get_state(self):
        return self.state, self.is_running

    def is_running(self):
        if self.thread is None:
            return False
        else:
            return self.thread.is_running


class ButtonNotifier:
    def __init__(self, state_light, button_pin, callback):
        self.state_light = state_light
        self.button = Button(pin=button_pin, callback=self._button_callback)
        self.callback = callback
        self.thread = None

    def _button_callback(self, pin, button_state):
        light_state, is_running = self.state_light.get_state()
        if button_state:
            self.state_light.start()
        else:
            self.stop()
            self.callback(pin, light_state, self)

    def is_running(self):
        if self.thread is None:
            return False
        else:
            return self.thread.is_running

    def stop(self):
        self.state_light.stop()


class TemperatureHumidity:
    def __init__(self, pin, centigrade=False):
        self.pin = pin
        self.temperature = None
        self.humidity = None
        self.worker_thread = None
        self.centigrade = centigrade

    def _get(self):
        logger = get_logger()
        if pio_loaded:
            self.humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.pin)
            if not self.centigrade:
                temp = 9.0/5.0 * temp + 32
            self.temperature = temp
            logger.debug("pin:{}, temp:{}, humidity:{}".format(self.pin, self.temperature, self.humidity))

    def start(self):
        self.worker_thread = WorkerThread(callback_function=self._get, sleep=1)
        self.worker_thread.start()

    def stop(self):
        self.worker_thread.stop()


class VibrationSensor:
    class Runner(threading.Thread):
        def __init__(self, parent_sensor):
            super(VibrationSensor.Runner, self).__init__()
            self.parent = parent_sensor
            logger = get_logger()
            logger.debug("creating a VibrationSensor.Runner")
            self.is_running = False
            self.jitter = 1000  # 1 mS
            self.changed_time = None
            self.changed_state = False
            self.last_time = datetime.datetime.now()

        def run(self):
            logger = get_logger()
            logger.debug("starting VibrationSensor.Runner")
            self.is_running = True
            while self.is_running:
                if self.changed_time is not None:
                    time_delay = (self.changed_time - self.last_time).microseconds
                    self.last_time = self.changed_time
                    print("delay:{}".format(time_delay))
                    if time_delay > self.jitter:
                        print("moving")

        # noinspection PyUnusedLocal
        def state_change(self, pin):
            print("called")
            self.changed_state = datetime.datetime.now()

    def __init__(self, pin, callback):
        self.pin = pin
        self.callback_function = callback
        self.thread = None
        self.last_change = datetime.datetime.now()
        self.last_state = False
        self.runner = None

    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        self.runner = VibrationSensor.Runner(self)
        self.runner.start()
        GPIO.add_event_detect(self.pin, GPIO.RISING, bouncetime=1)
        GPIO.add_event_callback(self.pin, self.runner.state_change)

    def _vibration_detected(self, pin):
        time_now = datetime.datetime.now()
        current_state = GPIO.input(pin)
        print("called:{}, {}, {}, {}".format(current_state, time_now, self.last_change,
                                             (time_now - self.last_change).microseconds))
        if current_state != self.last_state:
            if (time_now - self.last_change).microseconds > 1000:
                print("time exceeded")
                if current_state:
                    print("movement")
                else:
                    print("no movement")
                self.last_state = current_state
                self.last_change = time_now


class Accelerometer:
    # ADXL345 constants
    EARTH_GRAVITY_MS2 = 9.80665
    SCALE_MULTIPLIER = 0.004

    DATA_FORMAT = 0x31
    BW_RATE = 0x2C
    POWER_CTL = 0x2D

    BW_RATE_1600HZ = 0x0F
    BW_RATE_800HZ = 0x0E
    BW_RATE_400HZ = 0x0D
    BW_RATE_200HZ = 0x0C
    BW_RATE_100HZ = 0x0B
    BW_RATE_50HZ = 0x0A
    BW_RATE_25HZ = 0x09

    RANGE_2G = 0x00
    RANGE_4G = 0x01
    RANGE_8G = 0x02
    RANGE_16G = 0x03

    MEASURE = 0x08
    AXIS_DATA = 0x32

    address = None

    def __init__(self, address=0x53,
                 bandwidth_rate_flag=BW_RATE_100HZ, range_flag=RANGE_2G):
        self.address = address
        if pio_loaded:
            # select the correct i2c bus for this revision of Raspberry Pi
            revision = ([line[12:-1]
                         for line in open('/proc/cpuinfo', 'r').readlines()
                         if line[:8] == "Revision"] + ['0000'])[0]
            self.bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)
        self.bus.write_byte_data(self.address, Accelerometer.BW_RATE, bandwidth_rate_flag)
        value = self.bus.read_byte_data(self.address, Accelerometer.DATA_FORMAT)
        value &= ~0x0F
        value |= range_flag
        value |= 0x08
        self.bus.write_byte_data(self.address, Accelerometer.DATA_FORMAT, value)
        self.bus.write_byte_data(self.address, Accelerometer.POWER_CTL, Accelerometer.MEASURE)

    def get_axis(self, g_force=False):
        data = self.bus.read_i2c_block_data(self.address, Accelerometer.AXIS_DATA, 6)
        now = datetime.datetime.now()
        x = data[0] | (data[1] << 8)
        if x & (1 << 16 - 1):
            x -= 1 << 16
        y = data[2] | (data[3] << 8)
        if y & (1 << 16 - 1):
            y -= 1 << 16
        z = data[4] | (data[5] << 8)
        if z & (1 << 16 - 1):
            z -= 1 << 16
        if g_force:
            x *= Accelerometer.SCALE_MULTIPLIER
            y *= Accelerometer.SCALE_MULTIPLIER
            z *= Accelerometer.SCALE_MULTIPLIER
        else:
            x *= Accelerometer.EARTH_GRAVITY_MS2
            y *= Accelerometer.EARTH_GRAVITY_MS2
            z *= Accelerometer.EARTH_GRAVITY_MS2
        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)
        return {"x": x, "y": y, "z": z, "time": now}


class Motor:
    def __init__(self, accelerometer, resting_values):
        self.accelerometer = accelerometer
        self.resting_values = resting_values
        self.movement_checker = None
        self.motor_running = False

    class MovementChecker(threading.Thread):
        check_frequency = .001
        value_count = 10

        def __init__(self, parent_motor, callback):
            super(Motor.MovementChecker, self).__init__()
            self.callback = callback
            self.parent_motor = parent_motor
            self.thread_is_running = False
            self.values = [{"x": None, "y": None, "z": None}] * self.value_count

        def run(self):
            last_entry = 0
            filled = False
            resting_called = running_called = False
            while self.thread_is_running:
                # keep the counter within this thread's internal buffer
                if last_entry == len(self.values) - 1:
                    last_entry = 0
                    filled = True
                else:
                    last_entry += 1
                self.values[last_entry] = self.parent_motor.accelerometer.get_axis(True)
                if filled:  # no checking occurs until the small array is filled with movement data
                    if self.is_resting():
                        self.parent_motor.motor_running = False
                        if not resting_called:  # have not called stopped callback
                            running_called = False
                            resting_called = True
                            threading.Thread(target=self.callback, args=(False, self.when_event_occurred()))
                    else:  # motor is moving
                        self.parent_motor.motor_running = True
                        if not running_called:  # have not called callback
                            running_called = True
                            resting_called = False
                            threading.Thread(target=self.callback, args=(True, self.when_event_occurred()))
                time.sleep(Motor.MovementChecker.check_frequency)

        def is_resting(self):
            avg_x = avg_y = avg_z = 0
            for value in self.values:
                avg_x += value["x"]
                avg_y += value["y"]
                avg_z += value["z"]
            avg_x /= len(self.values)
            avg_y /= len(self.values)
            avg_z /= len(self.values)
            if avg_x > self.parent_motor.resting_values["x"] or \
               avg_y > self.parent_motor.resting_values["y"] or \
               avg_z > self.parent_motor.resting_values["z"]:
                return True
            else:
                return False

        def when_event_occurred(self):
            for value in self.values:
                if self.parent_motor.motor_running:  # look for when the motor first started moving
                    if value["x"] > self.parent_motor.resting_values["x"] or \
                       value["y"] > self.parent_motor.resting_values["y"] or \
                       value["z"] > self.parent_motor.resting_values["z"]:
                        return value["time"]
                else:  # look for when the motor first stopped moving
                    if value["x"] < self.parent_motor.resting_values["x"] or \
                       value["y"] < self.parent_motor.resting_values["y"] or \
                       value["z"] < self.parent_motor.resting_values["z"]:
                        return value["time"]

    def start(self, callback):
        Motor.MovementChecker(self, callback).start()

    @staticmethod
    def get_resting_values(accelerometer, duration_in_mils):
        start_time = datetime.datetime.now()
        min_x = min_y = min_z = sys.float_info.max
        max_x = max_y = max_z = 0
        while True:
            values = accelerometer.get_axis(True)
            if values["x"] > max_x:
                max_x = values["x"]
            if values["x"] < min_x:
                min_x = values["x"]
            if values["y"] > max_y:
                max_y = values["y"]
            if values["y"] < min_y:
                min_y = values["y"]
            if values["z"] > max_z:
                max_z = values["z"]
            if values["z"] < min_z:
                min_z = values["z"]
            if (datetime.datetime.now() - start_time).total_seconds() * 1000 >= duration_in_mils:
                break
            time.sleep(.001)

        return {"x": {"max": max_x, "min": min_x},
                "y": {"max": max_y, "min": min_y},
                "z": {"max": max_z, "min": min_z}
                }

    def is_moving(self):
        return self.motor_running


def the_callback(is_running, event_time):
    logger = get_logger()
    if is_running:
        logger.info("motor started at:{}".format(event_time))
    else:
        logger.info("motor stopped at:{}".format(event_time))


if __name__ == '__main__':
    if pio_loaded:
        print('PIO successfully loaded')
    else:
        print('PIO load unsuccessful!')
        sys.exit(0)
    test_accelerometer = False
    test_color_led = True
    if test_color_led:
        color_led = ColorLed(18, 23, 24)
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
    if test_accelerometer:
        acc = Accelerometer()
        static_motor_values = Motor.get_resting_values(acc, 2000)
        motor = Motor(acc, static_motor_values)
        motor.start(the_callback)

        while True:
            print("motor is running:{}".format(motor.is_moving()))
            time.sleep(.5)
