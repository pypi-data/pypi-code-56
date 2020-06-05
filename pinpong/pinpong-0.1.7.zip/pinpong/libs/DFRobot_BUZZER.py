import time
from pinpong.pinpong import *

class DFRobot_BUZZER:
  def __init__(self, board, obj):
    self.pin_obj  = obj
    self.board = board
    self.board.board.set_pin_mode_tone(self.pin_obj.pin)
    self.freq_value = 1000

  def on(self):
    self.board.board.play_tone(self.pin_obj.pin, self.freq_value, 0)

  def off(self):
    self.board.board.play_tone(self.pin_obj.pin, 0, 0)

  def freq(self, v=-1):
    if v == -1:
      return self.freq_value
    else:
      self.freq_value = v

  def tone(self, freq, duration):
    self.board.play_tone(self.pin_obj.pin, freq, duration)