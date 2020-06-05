import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_DHT import *


uno = PinPong("uno","com99")
uno.connect()

dht11 = DFRobot_DHT11(uno, Pin(uno,Pin.D7))
dht22 = DFRobot_DHT22(uno, Pin(uno,Pin.D6))

while True:
  temp = dht11.temperature()
  humi = dht11.humidity()
  print("dht11 temperature=",temp," humidity=",humi)
  
  temp = dht22.temperature()
  humi = dht22.humidity()
  print("dht11 temperature=",temp," humidity=",humi)
  time.sleep(1)


