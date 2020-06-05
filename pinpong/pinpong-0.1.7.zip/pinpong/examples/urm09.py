import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_URM09 import *

board = PinPong("uno", "com99")
board.connect()


urm = DFRobot_URM09(board,0x20)
urm.set_mode_range(urm._MEASURE_MODE_AUTOMATIC ,urm._MEASURE_RANG_500)

while True:
  dist =urm.get_distance()
  temp = urm.get_temperature()

  print("Temperature is %.2f .c    "%temp)
  print("Distance is %d cm         "%dist)
  time.sleep(0.5)
