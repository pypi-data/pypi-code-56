from time import sleep_ms
from machine import I2C, Pin
import sys

class xCore:
    def __init__(self, freq=100000):
        if sys.platform == "esp8266":
            scl=14
            sda=2
        else:
            scl=22
            sda=21

        self.i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)

    def write_read(self, addr, reg, length, repeat=False):
        self.i2c.writeto(addr, bytearray([reg]), repeat)
        raw = self.i2c.readfrom(addr, length)
        return raw

    def write_bytes(self, addr, *args, repeat=False):
        self.i2c.writeto(addr, bytes(args))

    def write(self, addr, buf, repeat=True):
        self.i2c.writeto(addr, buf, repeat)

    def read(self, addr, length, repeat=False):
        raw = self.i2c.readfrom(addr, length)
        return raw

    def writev(self, addr, vec, repeat=True):
        self.i2c.writevto(addr, vec, repeat)

    def sleep(time):
        sleep_ms(time)

    def stop(self):
        self.i2c.stop()

    def start(self):
        self.i2c.start()

    def write_(self, val):
        self.i2c.write(val)
