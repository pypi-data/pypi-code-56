import time
from pinpong.pinpong import *

class DFRobot_DHT11:
  def __init__(self,board, obj):
    self.board = board
    self.pin_obj = obj
    self.type = 11
    self.board.board.set_pin_mode_dht(self.pin_obj.pin, self.type, differential=.01)

  def measure(self):
    self.value = self.board.board.dht_read(self.pin_obj.pin)

  def temperature(self):
    return self.board.board.dht_read(self.pin_obj.pin)[1]

  def humidity(self):
    return self.board.board.dht_read(self.pin_obj.pin)[0]

class DFRobot_DHT22:
  def __init__(self,board, obj):
    self.board = board
    self.pin_obj = obj
    self.type = 22
    self.board.board.set_pin_mode_dht(self.pin_obj.pin, self.type, differential=.01)

  def measure(self):
    self.value = self.board.board.dht_read(self.pin_obj.pin)

  def temperature(self):
    return self.board.board.dht_read(self.pin_obj.pin)[1]

  def humidity(self):
    return self.board.board.dht_read(self.pin_obj.pin)[0]
