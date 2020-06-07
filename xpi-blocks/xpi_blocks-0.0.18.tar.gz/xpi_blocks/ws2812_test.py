
import board
#import RPi.GPIO as GPIO
import neopixel

# GPIO.setmode(GPIO.BCM)
pixels = neopixel.NeoPixel(board.D18, 1)

pixels[0] = (255, 0, 0)
sleep(2)
pixels[0] = (0, 255, 0)
