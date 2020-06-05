import time
from pinpong.pinpong import *

class DFRobot_HCSR04:
  def __init__(self,board,trigger_pin_obj, echo_pin_obj):
    self.board  = board
    self.trigger_pin_obj = trigger_pin_obj
    self.echo_pin_obj = echo_pin_obj
    self.board.board.set_pin_mode_sonar(self.trigger_pin_obj.pin, self.echo_pin_obj.pin)

  def read(self):
    return self.board.board.sonar_read(self.trigger_pin_obj.pin)[0]