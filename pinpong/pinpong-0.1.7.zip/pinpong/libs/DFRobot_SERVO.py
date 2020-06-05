import time
from pinpong.pinpong import *

class DFRobot_SERVO:
  def __init__(self, board, obj):
    self.board = board
    self.pin_obj = obj
    self.board.board.set_pin_mode_servo(self.pin_obj.pin)

  def angle(self, value):
    self.board.board.servo_write(self.pin_obj.pin, value)

