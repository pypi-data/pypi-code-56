from machine import Pin, TouchPad, I2C, SDCard
#from machine import Pin, TouchPad, I2C, I2S, SDCard
import sys, os, machine
import esp32, neopixel
from time import sleep

NP_PIN = Pin(0)
led = neopixel.NeoPixel(NP_PIN, 1)

try:
    os.mount(SDCard(), "/sd")
    led.fill((0,255,0))
    print('LOG SD Card mounted.')
except:
    led.fill((255,0,0))
    print('ERROR Could not Mount SD Card!')

led.write()

print('LOG app_b finished')
