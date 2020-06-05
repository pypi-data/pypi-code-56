import sys
import time
from pinpong.pinpong import *

board = PinPong("uno","com99")
board.connect()
d13 = Pin(board, Pin.D13, Pin.OUT)

while True:
  d13.value(0)
  time.sleep(1)

  d13.value(1)
  time.sleep(1)
