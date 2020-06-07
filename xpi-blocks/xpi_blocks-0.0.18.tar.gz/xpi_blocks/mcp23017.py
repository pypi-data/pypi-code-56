
# TODO: add serial operations


import smbus_m
import time
import sys
import ctypes

c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16
c_uint32 = ctypes.c_uint32


class Flag_bits(ctypes.Structure):
    _fields_ = [("rangeNumber", c_uint16, 4),
	    ("conversionTime", c_uint16, 1),
	    ("modeOfConversion", c_uint16, 2),
	    ("overflowFlag", c_uint16, 1),
	    ("conversionReady", c_uint16, 1),
	    ("flagHigh", c_uint16, 1),
	    ("flagLow", c_uint16, 1),
	    ("latch", c_uint16, 1),
	    ("polarity", c_uint16, 1),
	    ("maskExponent", c_uint16, 1),
	    ("faultCount", c_uint16, 2)]


class Flags(ctypes.Union):
    _fields_ = [("b", Flag_bits),
		("asshort", c_uint16)]


# ------- config the chip MCP23017 I2C Port Expander --------
# from MCP23017_I2C import *
#	GPIO_CHIP = GPIO_CHIP(0x20, 1)
#	 	    GPIO_CHIP( Device address, Pi Model )
# 0 = Model A, B Rev 2 or B+ Pi ; 1 = Model B Rev 1 Pi)


class MCP230xx:
	def __init__(self, bus_id, device_address):
			self.device_address = device_address  # DEVICE
			self.pi_model = pi_model
			self.bus = smbus.SMBus3(bus_id)

			self.act_ioA = 0x00
			self.act_ioB = 0x00
			self.act_pinA = 0x00
			self.act_pinB = 0x00

			self.IODIRB = 0x01  # Pin direction register
			self.IODIRA = 0x00  # Pin direction register
			self.OLATA = 0x14  # Register for outputs
			self.OLATB = 0x15  # Register for outputs
			self.GPIOA = 0x12  # Register for inputs
			self.GPIOB = 0x13  # Register for inputs

	def setup(self, pin, io, side):
	# GPIO_CHIP.setup( 0, 'OUT', 'A')
	# pin (0,7)  io (IN,OUT)  side (A,B)
		try:

			if (pin < 0 or pin > 7) or (side != 'A' and side != 'B') or (io != 'IN' and io != 'OUT'):
				print ' --- GPIO.setup(pin, io, side) ---'
				print ' --- pin (0 - 7)  io (IN or OUT)  side (A or B) ---'
				return;
			else:

				if io == 'IN' and side == 'A':
					pinio = self.act_ioA | (1 << pin)
					self.act_ioA = pinio
				else:
					if io == 'OUT' and side == 'A':
						pinio = self.act_ioA & ~(1 << pin)
						self.act_ioA = pinio
					else:
						if io == 'IN' and side == 'B':
							pinio = self.act_ioB | (1 << pin)
							self.act_ioB = pinio
						else:
							if io == 'OUT' and side == 'B':
								pinio = self.act_ioB & ~(1 << pin)
								self.act_ioB = pinio

				if side == 'A':
					self.bus.write_byte_data(self.device_address, self.IODIRA, pinio)
				else:
					self.bus.write_byte_data(self.device_address, self.IODIRB, pinio)

			return;

		except:
			print ' --- Error accessing the chip MCP23017 ---'
			raise

	def output(self, pin, hl, side):
	# GPIO_CHIP.output(0, 1, 'A')
	# pin (0,7)  hl (0,1)  side (A,B)
		try:

			if (pin < 0 or pin > 7) or (side != 'A' and side != 'B') or (hl != 1 and hl != 0):
				print ' --- GPIO.output(pin, hl, side) ---'
				print ' --- pin (0 - 7)  hl (0 or 1)  side (A or B) ---'
				return;
			else:
				if hl == 1 and side == 'A':
					pinhl = self.act_pinA | (1 << pin)
					self.act_pinA = pinhl
				else:
					if hl == 0 and side == 'A':
						pinhl = self.act_pinA & ~(1 << pin)
						self.act_pinA = pinhl
					else:
						if hl == 1 and side == 'B':
							pinhl = self.act_pinB | (1 << pin)
							self.act_pinB = pinhl
						else:
							if hl == 0 and side == 'B':
								pinhl = self.act_pinB & ~(1 << pin)
								self.act_pinB = pinhl
				if side == 'A':
					self.bus.write_byte_data(self.device_address, self.OLATA, pinhl)
				else:
					self.bus.write_byte_data(self.device_address, self.OLATB, pinhl)

			return;

		except:
			print ' --- Error accessing the chip MCP23017 ---'
			raise

	def input(self, pin, side):
	# Teste = GPIO_CHIP.input(7, 'B', port_expander)
	# 	pin (0,7)  side (A,B)
		try:
			if (pin < 0 or pin > 7) or (side != 'A' and side != 'B'):
				print ' --- MySwitch = GPIO.input(pin, side) ---'
				print ' --- pin (0 - 7)  side (A or B) ---'
				return;
			else:
				if side == 'A':
					MySwitch = self.bus.read_byte_data(self.device_address, self.GPIOA)
					if MySwitch & (1 << pin) == (1 << pin):
						MySwitch = 1
					else:
						MySwitch = 0
				else:
					MySwitch = self.bus.read_byte_data(self.device_address, self.GPIOB)
					if MySwitch & (1 << pin) == (1 << pin):
						MySwitch = 1
					else:
						MySwitch = 0

			return MySwitch;
		except:
			print ' --- Error accessing the chip MCP23017 ---'
			raise


def main():
	print "=========================================================="
	print "MCP23017 demo for RPI series"
	print "=========================================================="
	time.sleep(0.5)

	bus = 1
	addr = 0x20

	gpio = MCP230xx(bus, addr)


  gpio.setup(0, 'OUT', 'A')
  gpio.setup(1, 'OUT', 'A')
  gpio.setup(2, 'OUT', 'A')
  gpio.setup(3, 'OUT', 'A')
  gpio.setup(4, 'OUT', 'A')
  gpio.setup(5, 'OUT', 'A')
  gpio.setup(6, 'OUT', 'A')
  gpio.setup(7, 'OUT', 'A')
  gpio.setup(0, 'OUT', 'B')
  gpio.setup(1, 'OUT', 'B')
  gpio.setup(2, 'OUT', 'B')
  gpio.setup(3, 'OUT', 'B')
  gpio.setup(4, 'OUT', 'B')
  gpio.setup(5, 'OUT', 'B')
  gpio.setup(6, 'OUT', 'B')
  gpio.setup(7, 'OUT', 'B')



	try:
		while True:
			s="(Ctrl-C to exit)  "
      
      gpio.output(0, 1, 'A')       
      time.sleep(0.5)
      gpio.output(1, 1, 'A')       
      time.sleep(0.5)
      gpio.output(2, 1, 'A')       
      time.sleep(0.5)
      gpio.output(3, 1, 'A')       
      time.sleep(0.5)
      gpio.output(4, 1, 'A')       
      time.sleep(0.5)
      gpio.output(5, 1, 'A')       
      time.sleep(0.5)
      gpio.output(6, 1, 'A')       
      time.sleep(0.5)
      gpio.output(7, 1, 'A')       

      gpio.output(0, 1, 'B')       
      time.sleep(0.5)
      gpio.output(1, 1, 'B')       
      time.sleep(0.5)
      gpio.output(2, 1, 'B')       
      time.sleep(0.5)
      gpio.output(3, 1, 'B')       
      time.sleep(0.5)
      gpio.output(4, 1, 'B')       
      time.sleep(0.5)
      gpio.output(5, 1, 'B')       
      time.sleep(0.5)
      gpio.output(6, 1, 'B')       
      time.sleep(0.5)
      gpio.output(7, 1, 'B')       

      gpio.output(0, 0, 'A')       
      time.sleep(0.5)
      gpio.output(1, 0, 'A')       
      time.sleep(0.5)
      gpio.output(2, 0, 'A')       
      time.sleep(0.5)
      gpio.output(3, 0, 'A')       
      time.sleep(0.5)
      gpio.output(4, 0, 'A')       
      time.sleep(0.5)
      gpio.output(5, 0, 'A')       
      time.sleep(0.5)
      gpio.output(6, 0, 'A')       
      time.sleep(0.5)
      gpio.output(7, 0, 'A') 
      
      gpio.output(0, 0, 'B')       
      time.sleep(0.5)
      gpio.output(1, 0, 'B')       
      time.sleep(0.5)
      gpio.output(2, 0, 'B')       
      time.sleep(0.5)
      gpio.output(3, 0, 'B')       
      time.sleep(0.5)
      gpio.output(4, 0, 'B')       
      time.sleep(0.5)
      gpio.output(5, 0, 'B')       
      time.sleep(0.5)
      gpio.output(6, 0, 'B')       
      time.sleep(0.5)
      gpio.output(7, 0, 'B')      

	except KeyboardInterrupt:
		# Ctrl-C to exit
		sys.exit(0)
		
		
	

if __name__ =="__main__":
    main()      
