# -*- coding: utf8 -*-
# (C) Fabrice Sincère
# MicroPython

"""This MicroPython module provides an i2c driver for Maxim-Dallas DS1621 \
DS1631 DS1631A DS1721 DS1731 high-precision digital thermometer and thermostat.

DS1621, DS1631, DS1631A : thermometer accuracy is ±0.5°C
DS1721, DS1731 : thermometer accuracy is ±1°C

DS1631A begin performing temperature conversion immediately at power-up.

DS1621, DS1631, DS1721 and DS1731 begins continuous conversions after \
a Start Convert command.

Datasheet
=========

https://datasheets.maximintegrated.com/en/ds/DS1621.pdf
https://datasheets.maximintegrated.com/en/ds/DS1721.pdf
https://datasheets.maximintegrated.com/en/ds/DS1631-DS1731.pdf

2-wire serial data bus
======================

DS1631s (8 devices max) are connected to your MicroPython board with 4 wires :

- SDA i2c bus (+ about 4.7 kΩ pull-up resistor)
- SCL i2c bus (+ about 4.7 kΩ pull-up resistor)
- Power (3.3 V)
- Ground

Note : successfully tested with ESP8266 NodeMCU, ESP32 WROOM-32D, \
STM32L476 Nucleo-64, STM32WB55 Nucleo board.

Installation
============

>>> import upip
>>> upip.install('micropython-ds1631')

Basic usage
===========

from machine import Pin, I2C
import time
import DS1631

# i2c bus pins
i2c = I2C(scl=Pin(4), sda=Pin(5))
# i2c bus scan
[print(hex(i)) for i in i2c.scan()]

i2c_address = 0x48
ic1 = DS1631.DS1631(i2c, i2c_address)
# thermostat config
ic1.set_tout_polarity("active-low")
ic1.set_thigh(24.5)
ic1.set_tlow(22.5)
# thermometer config
ic1.set_conversion_mode("continuous")
ic1.set_resolution(12)
ic1.start_convert()
# read temperature
while True:
    time.sleep_ms(750)
    temperature = ic1.get_temperature()
    print("Temperature  : {} °C".format(temperature))


Author
======

Fabrice Sincère <fabrice.sincere@wanadoo.fr>
https://pypi.org/project/micropython-ds1631
https://framagit.org/fsincere/micropython-ds1631

History release
===============
0.4.6 : add git repository
"""

import ustruct

__version__ = (0, 4, 6)
__author__ = "Fabrice Sincère <fabrice.sincere@wanadoo.fr>"


class DS1631:
    """MicroPython i2c driver for Maxim-Dallas DS1621 \
DS1631 DS1631A DS1721 DS1731"""

    # command set
    ACCESS_CONFIG = const(0xAC)  # 1 byte, read/write
    READ_TEMPERATURE = const(0xAA)  # 2 bytes, read only
    ACCESS_TH = const(0xA1)  # 2 bytes, read/write
    ACCESS_TL = const(0xA2)  # 2 bytes, read/write

    START_CONVERT = const(0x51)
    STOP_CONVERT = const(0x22)
    SOFTWARE_POR = const(0x54)

    def __init__(self, I2C_object, i2c_addr):
        """i2c_addr : 7-bit i2c address is (1 0 0 1 A2 A1 A0)

Basic usage
-----------

from machine import Pin, I2C
import DS1631

i2c = I2C(scl=Pin(4), sda=Pin(5))

sensor = DS1631.DS1631(i2c, 0x48)
sensor.print_configuration()
"""
        self.i2c = I2C_object

        # 7-bit i2c address is (1 0 0 1 A2 A1 A0)
        self.i2c_addr = i2c_addr

        if self.i2c_addr not in range(0x48, 0x4F + 1):
            raise ValueError("Invalid i2c address")

    def set_conversion_mode(self, mode):
        """Set the conversion mode
mode = "one-shot" or "continuous"
Stored in EEPROM (write cycle time : 10 ms max)

Note : when writing to the configuration register, conversions should first be \
stopped using the Stop Convert command if the device is in continuous \
conversion mode.
"""
        config_register = self.get_config_register()
        # 1SHOT : Configuration Register Bit 0 (LSB)
        # write 1SHOT bit

        if mode == "one-shot":
            # one-shot mode (1SHOT = 1)
            self.set_config_register(config_register | 0x01)
        elif mode == "continuous":
            # continuous mode (1SHOT = 0)
            self.set_config_register(config_register & 0xFE)
        else:
            raise NameError("Invalid conversion mode name")

    def get_conversion_mode(self, config_register=None):
        """Read and return the conversion mode ("continuous" or "one-shot")"""

        if config_register is None:
            # Read config register
            config_register = self.get_config_register()
        # read 1SHOT bit
        if config_register & 0x01 == 0x00:
            # continuous mode (1SHOT = 0)
            return "continuous"
        else:
            # one-shot mode (1SHOT = 1)
            return "one-shot"

    def set_tout_polarity(self, polarity):
        """Set the Tout polarity
polarity = "active-low" or "active-high"
Stored in EEPROM (write cycle time : 10 ms max)

Note : when writing to the configuration register, conversions should first \
be stopped using the Stop Convert command if the device is in \
continuous conversion mode.
"""
        config_register = self.get_config_register()
        # Tout polarity : POL Configuration Register Bit 1
        # write POL bit
        if polarity == "active-high":
            # POL = 1
            self.set_config_register(config_register | 0x02)
        elif polarity == "active-low":
            # POL = 0
            self.set_config_register(config_register & 0xFD)
        else:
            raise NameError("Invalid polarity name")

    def get_tout_polarity(self, config_register=None):
        """Read and return the Tout polarity ("active-low" or "active-high")"""
        if config_register is None:
            # Read config register
            config_register = self.get_config_register()
        # Tout polarity : POL (bit 1)
        if config_register & 0x02 == 0x00:
            # POL = 0
            return "active-low"
        else:
            # POL = 1
            return "active-high"

    def set_resolution(self, resolution):
        """Set the temperature resolution
resolution is 9, 10, 11 or 12 bits

Stored in SRAM (power-up state 12 bits)

Note : when writing to the configuration register, conversions should first be \
stopped using the Stop Convert command if the device is in \
continuous conversion mode.
"""
        config_register = self.get_config_register()
        # write R1 (bit 3) R0 (bit 2)
        if resolution == 9:
            # R1 = 0 R0 = 0
            self.set_config_register(config_register & 0xF3)
        elif resolution == 10:
            # R1 = 0 R0 = 1
            self.set_config_register((config_register & 0xF7) | 0x04)
        elif resolution == 11:
            # R1 = 1 R0 = 0
            self.set_config_register((config_register & 0xFB) | 0x08)
        elif resolution == 12:
            # R1 = 1 R0 = 1
            self.set_config_register(config_register | 0x0C)
        else:
            raise ValueError("Resolution out of range")

    def get_resolution(self, config_register=None):
        """Read resolution and return the tuple \
temperature resolution (bits), temperature resolution (°C), \
conversion time (ms)"""

        if config_register is None:
            # Read config register
            config_register = self.get_config_register()

        # resolution : R1 (bit 3) R0 (bit 2)
        if config_register & 0x0C == 0x00:
            # R1=0  R0=0
            return 9, 0.5, 93.75
        elif config_register & 0x0C == 0x04:
            # R1=0  R0=1
            return 10, 0.25, 187.5
        elif config_register & 0x0C == 0x08:
            # R1=1  R0=0
            return 11, 0.125, 375.0
        elif config_register & 0x0C == 0x0C:
            # R1=1  R0=1
            return 12, 0.0625, 750.0

    def is_eeprom_busy(self, config_register=None):
        """EEPROM status
return True if a write to memory is in progress
return False if memory is not busy

Note : write cycle time : 10 ms max, 4 ms typ.
"""
        if config_register is None:
            # Read the NVB (NV Memory Busy) bit from config register
            config_register = self.get_config_register()

        # Non Volatile Memory Busy : NVB (bit 4)
        if config_register & 0x10 == 0x00:
            # NVB = 0 : memory is not busy
            return False
        else:
            # NVB = 1 : a write to memory is in progress
            return True

    def is_tlow_flag_on(self, config_register=None):
        """Tl thermostat status.
return False if the measured temperature has not been lower than the \
value stored in the Tl register since power-up ;
otherwise return True
"""
        if config_register is None:
            # Read config register
            config_register = self.get_config_register()

        # Temperature Low Flag : TLF (bit 5)
        if config_register & 0x20 == 0x00:
            # TLF = 0 "off"
            return False
        else:
            # TLF = 1 "on"
            return True

    def reset_tlow_flag(self):
        """Tl thermostat status.
Tlow flag is overwritten with a 0
"""
        config_register = self.get_config_register()
        # Temperature Low Flag : TLF (bit 5)
        # reset TLF
        self.set_config_register(config_register & 0xDF)

    def is_thigh_flag_on(self, config_register=None):
        """Th thermostat status.
return False if the measured temperature has not exceeded the value \
stored in the Th register since power-up ;
otherwise return True
"""
        if config_register is None:
            # Read Temperature High Flag bit
            config_register = self.get_config_register()

        # Temperature High Flag : THF (bit 6)
        if config_register & 0x40 == 0x00:
            # THF = 0 "off"
            return False
        else:
            # THF = 1 "on"
            return True

    def reset_thigh_flag(self):
        """Th thermostat status.
Thigh flag is overwritten with a 0
"""
        config_register = self.get_config_register()
        # Temperature High Flag : THF (bit 6)
        # reset THF
        self.set_config_register(config_register & 0xBF)

    def is_temperature_conversion_in_progress(self, config_register=None):
        """Temperature conversion status
return True if a temperature conversion is in progress
return False if the temperature conversion is complete
"""
        if config_register is None:
            # Read the DONE bit from config register
            config_register = self.get_config_register()

        # Temperature Conversion : DONE (bit 7)
        if config_register & 0x80 == 0x00:
            # DONE = 0 'in progress'
            return True
        else:
            # DONE = 1 'complete'
            return False

    def get_temperature(self):
        """Read and return the last converted temperature value (°C) \
from the temperature register.

Note : temperature value stored in SRAM (power-up state -60 °C)
"""
        word = self.i2c.readfrom_mem(self.i2c_addr, DS1631.READ_TEMPERATURE, 2)
        return convert_word_to_temperature(word)

    def set_thigh(self, temperature):
        """Set the upper thermostat trip point.
temperature range : -55°C to +125°C
Stored in EEPROM (write cycle time : 10 ms max)

Note : when making changes to the Th and Tl registers, conversions should \
first be stopped using the Stop Convert command if the device is in \
continuous conversion mode.
"""

        if not -55.0 <= temperature <= 125.0:
            raise ValueError("Temperature out of range")

        self.i2c.writeto_mem(self.i2c_addr, DS1631.ACCESS_TH,
                             convert_temperature_to_word(temperature))

    def get_thigh(self):
        """Read and return the Th thermostat register (°C)"""
        word = self.i2c.readfrom_mem(self.i2c_addr, DS1631.ACCESS_TH, 2)
        return convert_word_to_temperature(word)

    def set_tlow(self, temperature):
        """Set the lower thermostat trip point.
temperature range : -55°C to +125°C
Stored in EEPROM (write cycle time : 10 ms max)

Note : when making changes to the Th and Tl registers, conversions should \
first be stopped using the Stop Convert command if the device is in continuous \
conversion mode.
"""
        if not -55.0 <= temperature <= 125.0:
            raise ValueError("Temperature out of range")

        self.i2c.writeto_mem(self.i2c_addr, DS1631.ACCESS_TL,
                             convert_temperature_to_word(temperature))

    def get_tlow(self):
        """Read and return the Tl thermostat register (°C)"""

        word = self.i2c.readfrom_mem(self.i2c_addr, DS1631.ACCESS_TL, 2)
        return convert_word_to_temperature(word)

    def start_convert(self):
        """Initiates temperature conversions.
If the part is in one-shot mode, only one conversion is performed.
In continuous mode, continuous temperature conversions are performed \
until a Stop Convert command is issued."""
        self.i2c.writeto(self.i2c_addr, bytes([DS1631.START_CONVERT]))

    def stop_convert(self):
        """Stops temperature conversions when the device is in
continuous conversion mode"""
        self.i2c.writeto(self.i2c_addr, bytes([DS1631.STOP_CONVERT]))

    def software_por(self):
        """ Initiates a software power-on-reset (POR), which stops \
temperature conversions and resets all registers and logic to their \
power-up states.

Power-up state
--------------

temperature register : -60 °C
resolution  : 12 bits
temperature high flag : 0 (off)
temperature low flag : 0 (off)
"""
        try:
            self.i2c.writeto(self.i2c_addr, bytes([DS1631.SOFTWARE_POR]))
        except:
            pass

    def get_config_register(self):
        """Read and return the configuration register"""
        config_register = \
            self.i2c.readfrom_mem(self.i2c_addr, DS1631.ACCESS_CONFIG, 1)
        return config_register[0]

    def set_config_register(self, config_register):
        """Write to the configuration register

Note : when writing to the configuration register, conversions should first be \
stopped using the Stop Convert command if the device is in \
continuous conversion mode."""
        self.i2c.writeto_mem(self.i2c_addr, DS1631.ACCESS_CONFIG,
                             bytes([config_register]))

    def print_configuration(self):
        """Read and print configuration and status information"""

        config_register = self.get_config_register()
        memory = self.is_eeprom_busy(config_register)
        conversion_mode = self.get_conversion_mode(config_register)
        tout_polarity = self.get_tout_polarity(config_register)
        resolution, quantum, conversion_time = \
            self.get_resolution(config_register)
        if memory:
            memory = "a write to memory is in progress"
        else:
            memory = "memory is not busy"
        tlow_flag = self.is_tlow_flag_on(config_register)
        if tlow_flag:
            tlow_flag = "on"
        else:
            tlow_flag = "off"
        thigh_flag = self.is_thigh_flag_on(config_register)
        if thigh_flag:
            thigh_flag = "on"
        else:
            thigh_flag = "off"
        temperature_conversion = \
            self.is_temperature_conversion_in_progress(config_register)
        if temperature_conversion:
            temperature_conversion = "in progress"
        else:
            temperature_conversion = "complete"

        print("""
Configuration
-------------
I2c address            : 0x{:0x}
Configuration register : 0x{:0x}

Conversion mode        : {}
Tout polarity          : {}
Resolution             : {} bits
 --> Resolution        : {} °C
 --> Conversion time   : {} ms (max)

Status information
------------------
EEPROM memory          : {}
Temperature Low Flag   : {}
Temperature High Flag  : {}
Temperature conversion : {}
""".format(self.i2c_addr, config_register, conversion_mode,
           tout_polarity, resolution, quantum, conversion_time, memory,
           tlow_flag, thigh_flag, temperature_conversion))


def convert_temperature_to_word(temperature):
    """temperature (float) : -55°C to +125°C range
Return a word (2 bytes) in big endian format"""
    # 16 bits two’s complement format
    word = int(temperature*256)
    return ustruct.pack('>h', word)


def convert_word_to_temperature(word):
    """word (2 bytes) in big endian format
Return temperature in °C (float)"""
    return ustruct.unpack('>h', word)[0]/256
