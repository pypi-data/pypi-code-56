import sys
import time
from pinpong.pinpong import *

uno = PinPong("uno","com99")
uno.connect()

adc0 = ADC(uno,Pin(uno, Pin.A0))
adc1 = ADC(uno,Pin(uno, Pin.A1))

while True:
  v = adc0.read()
  print("A0=", v)
  v = adc1.read()
  print("A1=", v)
  time.sleep(0.5)
