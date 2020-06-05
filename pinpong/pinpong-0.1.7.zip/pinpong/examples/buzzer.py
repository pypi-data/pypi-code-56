import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_BUZZER import *

uno = PinPong("uno","com99")
uno.connect()

buzzer = DFRobot_BUZZER(uno, Pin(uno,Pin.D7))
buzzer.freq(200)

while True:
  print("freq=",buzzer.freq())
  buzzer.on()
  time.sleep(1)
  buzzer.off()
  time.sleep(1)
  buzzer.freq(buzzer.freq()+100)