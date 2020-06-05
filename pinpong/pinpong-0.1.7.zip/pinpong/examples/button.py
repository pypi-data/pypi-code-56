import sys
import time
from pinpong.pinpong import *

board = PinPong("uno","com99")
board.connect()

btn = Pin(board, Pin.D8, Pin.IN)
led = Pin(board, Pin.D13, Pin.OUT)

while True:
  v = btn.value()
  #print(v)
  led.value(v)
  time.sleep(0.1)
