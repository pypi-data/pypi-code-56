import sys
import time
from pinpong.pinpong import *

uno = PinPong("uno","com99")
uno.connect()
pwm0 = PWM(uno,Pin(uno,Pin.D6))

while True:
  for i in range(255):
    print(i)
    pwm0.duty(i)
    time.sleep(0.05)
