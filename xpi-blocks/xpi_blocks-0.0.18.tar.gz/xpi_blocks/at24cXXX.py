
# **********************************************************************;
# * Project           : xPILib
# *
# * Program name      : at24cXXX.py (AT24C64, AT24C128, AT24C256)
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20191121
# *
# * Purpose           : Managing I2C EEPROM memory module
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 201911    Viacheslav Karpizin      1      original version
# *
#
# Copyright (c) 2019, Viacheslav Karpizin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# **********************************************************************


# AT24C32A, 32K (32768 kbit / 4 KB), 128 pages, 32 bytes per page, i2c addr 0x50

import time


class AT24C32N(object):
    """Driver for the AT24C32N 32K EEPROM."""

    def __init__(self, i2c, i2c_addr=0x50, pages=128, bpp=32):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.pages = pages
        self.bpp = bpp  # bytes per page

    def capacity(self):
        """Storage capacity in bytes"""
        return self.pages * self.bpp

    def read(self, addr, nbytes):
        """Read one or more bytes from the EEPROM starting from a specific address"""
        return self.i2c.readfrom_mem(self.i2c_addr, addr, nbytes, addrsize=16)

    def write(self, addr, buf):
        """Write one or more bytes to the EEPROM starting from a specific address"""
        offset = addr % self.bpp
        partial = 0
        # partial page write
        if offset > 0:
            partial = self.bpp - offset
            self.i2c.writeto_mem(self.i2c_addr, addr,
                                 buf[0:partial], addrsize=16)
            time.sleep_ms(5)
            addr += partial
        # full page write
        for i in range(partial, len(buf), self.bpp):
            self.i2c.writeto_mem(self.i2c_addr, addr+i -
                                 partial, buf[i:i+self.bpp], addrsize=16)
            time.sleep_ms(5)


# define FULL_MASK 0x7FFFF
# define DEVICE_MASK 0x7F0000
# define WORD_MASK 0xFFFF

class AT24CXXX:
  def __init__(self, bus_id, addr):
		self._address = addr
    self._bus = smbus_m.SMBus3(bus_id)
    return
    
    
    
  def write(self, dataAddress, data):
    Wire.beginTransmission((uint8_t)((0x500000 | dataAddress) >> 16)); // B1010xxx
    self._bus.write_byte(self._address, (0x500000 | dataAddress) >> 16)
    Wire.write((uint8_t)((dataAddress & WORD_MASK) >> 8)); // MSB
    Wire.write((uint8_t)(dataAddress & 0xFF)); // LSB
    Wire.write(data);
    Wire.endTransmission();
    delay(5);    
    
    
  def read(self, dataAddress):
    uint8_t data = 0x00;
    Wire.beginTransmission((uint8_t)((0x500000 | dataAddress) >> 16)); // B1010xxx
    Wire.write((uint8_t)((dataAddress & WORD_MASK) >> 8)); // MSB
    Wire.write((uint8_t)(dataAddress & 0xFF)); // LSB
    Wire.endTransmission();
    Wire.requestFrom((uint8_t)((0x500000 | dataAddress) >> 16),(uint8_t)1);
    if (Wire.available()) 
      data = Wire.peek()
    return data;    
    


def main():
	print("==========================================================")
	print("AT24CXXX demo for RPI series")
	print("==========================================================")
	time.sleep(0.5)
	
	bus = 1
	addr =  0x44
	
	memChip = AT24CXXX(bus, addr)
	


	try:
		while True:

	except KeyboardInterrupt:
		# Ctrl-C to exit
		sys.exit(0)
		
		
	

if __name__ =="__main__":
    main()



