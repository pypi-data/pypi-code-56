import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_NEOPIXEL import *

NEOPIXEL_PIN = Pin.A4
PIXELS_NUM = 4

board = PinPong("uno","com99")
board.connect()
np = DFRobot_NEOPIXEL(board, Pin(board,NEOPIXEL_PIN),PIXELS_NUM)

while True:
  np[0] = (0, 255 ,0)
  np[1] = (255, 0, 0)
  np[2] = (0, 0, 255)
  np[3] = (255, 0, 255)
  time.sleep(1)
  np[1] = (0, 255, 0)
  np[2] = (255, 0, 0)
  np[3] = (255, 255, 0)
  np[0] = (0, 0, 255)
  time.sleep(1)
