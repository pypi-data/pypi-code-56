import os
import time
import serial
import platform
import serial.tools.list_ports

from pinpong.base.avrdude import *
from pinpong.base import pymata4

OUTPUT = 0
INPUT = 1
ANALOG = 2
PWM = 3
SERVO = 4
NEOPIXEL = 5

PINPONG_MAJOR=0
PINPONG_MINOR=1
PINPONG_DELTA=7

FIRMATA_MAJOR = 2
FIRMATA_MINOR = 6

gboard = None

def get_pin(board,vpin):
  if board.boardname == "UNO" or board.boardname == "LEONARDO":
    dpin = vpin if vpin<20 else (vpin-100+14) if vpin >= 100 else -1
    apin = vpin-100 if vpin >= 100 else -1
  return dpin,apin

class Pin:
  D0 = 0
  D1 = 1
  D2 = 2
  D3 = 3
  D4 = 4
  D5 = 5
  D6 = 6
  D7 = 7
  D8 = 8
  D9 = 9
  D10 = 10
  D11 = 11
  D12 = 12
  D13 = 13
  D14 = 14
  D15 = 15
  D16 = 16
  D17 = 17
  D18 = 18
  D19 = 19
  D20 = 20
  D21 = 21
  D22 = 22
  D23 = 23
  D24 = 24
  D25 = 25
  D26 = 26
  D27 = 27
  D28 = 28
  D29 = 29
  D30 = 30
  D31 = 31
  D32 = 32
  D33 = 33
  D34 = 34
  D35 = 35
  D36 = 36
  D37 = 37
  D38 = 38
  D39 = 39
  D40 = 40
  D41 = 41
  D42 = 42
  D43 = 43
  D44 = 44
  D45 = 45
  D46 = 46
  D47 = 47
  D48 = 48
  D49 = 49
  D50 = 50
  D51 = 51
  D52 = 52
  
  A0 = 100
  A1 = 101
  A2 = 102
  A3 = 103
  A4 = 104
  A5 = 105
  
  IN = 1
  OUT = 3
  IRQ_FALLING = 2
  IRQ_RISING = 1
  IRQ_DRAIN = 7
  PULL_DOWN = 1
  PULL_UP = 2

  def __init__(self, board, vpin, mode=None):
    self.board = board
    self.pin,self.apin = get_pin(self.board, vpin)
    self.mode = mode
    if(mode == self.OUT):
      self.board.board.set_pin_mode_digital_output(self.pin)
    elif(mode == self.IN):
      self.board.board.set_pin_mode_digital_input(self.pin, callback=None)
    #elif(mode == PWM):
    #  self.board.board.set_pin_mode_pwm_output(self.pin)
    #elif(mode == ANALOG):
    #  self.board.board.set_pin_mode_analog_input(self.apin, callback)
    #elif(mode == SERVO):
    #  self.board.board.set_pin_mode_servo(self.pin)
    #elif(mode == NEOPIXEL):
    #  self.board.board.set_pin_mode_neo(self.pin)

  def value(self, v = -1):
    if v == -1:
      self.v = self.board.board.digital_read(self.pin)
      return self.v
    else:
      self.board.board.digital_pin_write(self.pin, v)
      time.sleep(0.001)

  def on(self):
    self.board.board.digital_pin_write(self.pin, 1)

  def off(self):
    self.board.board.digital_pin_write(self.pin, 0)
  
  def irq(self, trigger, handler):
    self.board.board.set_pin_mode_digital_input(self.pin, handler)
    self.board.board.set_digital_pin_params(self.pin, trigger, handler)

class ADC:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_analog_input(self.pin_obj.apin, None)

  def read(self):
    return self.board.board.analog_read(self.pin_obj.apin)

class PWM:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_pwm_output(self.pin_obj.pin)
    self.freq_value = 0
    self.duty_value = 0

  def freq(self, v=-1):
    if v == -1:
      return self.freq_value
    else:
      self.freq_value = v
      #self.board.board.pwm_write(self.pin_obj.pin, self.freq_value)

  def duty(self, v=-1):
    if v == -1:
      return self.duty_value
    else:
      self.duty_value = v
      self.board.board.pwm_write(self.pin_obj.pin, self.duty_value)

  def deinit(self):
    self.board.board.set_pin_mode_digital_input(self.pin_obj.pin, callback=None)

class PinPong:
  def __init__(self, boardname, port):
    global gboard
    self.boardname = boardname.upper()
    self.port = port
    self._iic_init = False
    gboard = self

  def printlogo(self):
    print("""
      ____  _       ____                   
     / __ \(_)___  / __ \____  ____  ____ _
    / /_/ / / __ \/ /_/ / __ \/ __ \/ __ `/
   / ____/ / / / / ____/ /_/ / / / / /_/ / 
  /_/   /_/_/ /_/_/    \____/_/ /_/\__, /  
     v%d.%d.%d  Designed by DFRobot  /____/ 
    """%(PINPONG_MAJOR,PINPONG_MINOR,PINPONG_DELTA))
    
  def connect(self):
    self.printlogo()
    major,minor = self.detect_firmata()
    print("Firmata Firmware verson V%d.%d"%(major,minor))
    if major != FIRMATA_MAJOR or minor != FIRMATA_MINOR:
      cwdpath,_ = os.path.split(os.path.realpath(__file__))
      pgm = Burner(self.boardname,self.port)
      if(self.boardname == "UNO"):
        name = platform.platform()
        if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial")>=0:
          cmd = "/home/scope/software/avrdude-6.3/avrdude -C/home/scope/software/avrdude-6.3/avrdude.conf -v -patmega328p -carduino -P"+self.port+" -b115200 -D -Uflash:w:"+cwdpath + "/base/FirmataExpress.Uno."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex"+":i"
          os.system(cmd)
        else:
          pgm.burn(cwdpath + "/base/FirmataExpress.Uno."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      elif(self.boardname == "LEONARDO"):
        port_list_0 = list(serial.tools.list_ports.comports())
        port_list_2 = port_list_0 = [list(x) for x in port_list_0]
        ser = serial.Serial(self.port,1200,timeout=1)
        ser.close()

        retry = 5
        port = None
        while retry:
          retry = retry - 1
          port_list_2 = list(serial.tools.list_ports.comports())
          port_list_2 = [list(x) for x in port_list_2]
          for p in port_list_2:
            if p not in port_list_0:
              port = p
              break
          if port == None:
            time.sleep(0.5)
          if port:
            print("port=====",port)
            break
        pgm = Burner(self.boardname,port[0])
        pgm.burn(cwdpath + "/base/FirmataExpress.Leonardo."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
    time.sleep(2)
    self.board = pymata4.Pymata4(com_port=self.port, baud_rate=115200)
    return True

  def detect_firmata(self):
    ser=serial.Serial(self.port, 115200, timeout=3)
    if(self.boardname == "UNO"):
      time.sleep(3)
    ser.read(ser.in_waiting)
    buf=bytearray(b"\xf0\x79\xf7")
    ser.write(buf)
    res = ser.read(10)
    if len(res) < 3:
      major=0
      minor=0
    elif res[0] == 0xF9:
      major = res[1]
      minor = res[2]
    elif res[0] == 0xF0 and res[1] == 0x79:
      major = res[2]
      minor = res[3]
    else:
      major=0
      minor=0
    ser.close()
    return major,minor

  def pin_mode(self, pin, mode, callback=None):
    if(mode == OUTPUT):
      self.board.set_pin_mode_digital_output(pin)
    elif(mode == INPUT):
      self.board.set_pin_mode_digital_input(pin, callback)
    elif(mode == PWM):
      self.board.set_pin_mode_pwm_output(pin)
    elif(mode == ANALOG):
      self.board.set_pin_mode_analog_input(apins[pin], callback)
    elif(mode == SERVO):
      self.board.set_pin_mode_servo(pin)
    elif(mode == NEOPIXEL):
      self.board.set_pin_mode_neo(pin)

  def write_digital(self, pin, value):
    self.board.digital_pin_write(pin, value)
    time.sleep(0.001)

  def read_digital(self, pin):
    return self.board.digital_read(pin)

  def read_analog(self, pin):
    return self.board.analog_read(apins[pin])

  def write_analog(self, pin, value):
    value = value*0x40
    self.board.pwm_write(pin, value)

  def servo_write_angle(self, pin, value):
    self.board.servo_write(pin, value)

  def neopixel_write(self, pin, value):
    self.board.neopixel_write(pin, value)

  def i2c_readfrom(self, address, register, read_byte):
    if not self._iic_init:
      self.board.set_pin_mode_i2c()
      self._iic_init = True
    return self.board.i2c_read(address, register, read_byte, None)

  def i2c_writeto(self, address, args):
    if not self._iic_init:
      self.board.set_pin_mode_i2c()
      self._iic_init = True
    self.board.i2c_write(address, args)