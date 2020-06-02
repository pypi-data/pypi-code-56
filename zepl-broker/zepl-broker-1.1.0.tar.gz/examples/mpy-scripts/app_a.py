import sys, os, machine
import select
import esp32
import neopixel

from time import sleep

NP_PIN = machine.Pin(0)
led = neopixel.NeoPixel(NP_PIN, 1)

led.fill((25,25,25))
led.write()

print('LOG app_a finished')
sleep(2)
