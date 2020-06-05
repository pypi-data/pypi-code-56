import time
from pinpong.pinpong import *

class DFRobot_NEOPIXEL(object):
  def __init__(self, board, pin_obj, num):
    self.pin_obj  = pin_obj
    self.board = board
    self.num = num
    self.__data = [(0,0,0) for i in range(num)]
    self.board.pin_mode(self.pin_obj.pin, NEOPIXEL)
    self.board.board.neopixel_config(self.pin_obj.pin,self.num)
    time.sleep(0.1)

  def __repr__(self):
    return 'pixel data (%s)' % self.__data
 
  def __getitem__(self, i):
    return self.__data[i]  # 返回data绑定列表中的第i个元素
 
  def __setitem__(self, i, v):
    #print(i,v)
    self.__data[i]=v
    self.board.board.neopixel_write(i,v)

  def write(self , n, r, g, b):
    self.board.board.neopixel_write(n,(r,g,b))
