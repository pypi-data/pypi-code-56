import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_HCSR04 import *

TRIGER_PIN = Pin.D7
ECHO_PIN = Pin.D8

board = PinPong("uno","com99")
board.connect()
sonar = DFRobot_HCSR04(board,Pin(board,TRIGER_PIN),Pin(board,ECHO_PIN))

while True:
  dis = sonar.read()
  print("distance = %d cm"%dis)
  time.sleep(0.1)
