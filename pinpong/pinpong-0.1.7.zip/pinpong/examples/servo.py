import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_SERVO import *

SERVO_PIN = Pin.D4

board = PinPong("uno","com4")
board.connect()

servo1 = DFRobot_SERVO(board, Pin(board,SERVO_PIN))

while True:
  servo1.angle(0)
  time.sleep(1)

  servo1.angle(90)
  time.sleep(1)

  servo1.angle(180)
  time.sleep(1)

  servo1.angle(90)
  time.sleep(1)