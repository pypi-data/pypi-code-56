
# **********************************************************************;
# * Project           : RPI_Blocks
# *
# * Program name      : HDC1080.py
# *
# * Author            : Viacheslav Karpizin
# *
# * Date created      : 20200410
# *
# * Purpose           : HDC1080 (CCS811) gas sensor
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202004    Viacheslav Karpizin      1      original version
# *
#
# Copyright (c) 2019, Viacheslav Karpizin, 2017 (c) Sai Yamanoor
#

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


import time


class CCS811(object):

    def __init__(self, device_bus=1, device_address=0x5A):
        self.device_bus = device_bus
        self.device_address = device_address
        self.bus = I2C("/dev/i2c-1")

    def start_app(self):
        self.write_byte(0xF4)
        print(self.read_byte(0x00))
        self.write_byte_data(0x01, 0x10)

    def transfer(self, msgs):
        try:
            self.bus.transfer(self.device_address, msgs)
        except I2CError as error:
            print(str(error))
        return msgs

    def close(self):
        self.bus.close()

    def read_byte(self, address):
        msgs = [I2C.Message([address], read=False)]
        self.transfer(msgs)
        msgs = [I2C.Message([address], read=True)]
        ret_msg = self.transfer(msgs)

        return (ret_msg[0].data[0])

    def write_byte(self, address):
        msgs = [I2C.Message([address], read=False)]
        self.transfer(msgs)

    def reset(self):
        msgs = [I2C.Message([0xFF, 0x11, 0xE5, 0x72, 0x8A], read=False)]
        self.transfer(msgs)

    def write_byte_data(self, address, data):
        msgs = [I2C.Message([address, data], read=False)]
        self.transfer(msgs)

    def read_bytes(self, count):
        msgs = [I2C.Message([0] * count, read=True)]
        ret_msg = self.transfer(msgs)
        return ret_msg[0].data


if __name__ == "__main__":
    my_ccs811 = CCS811()
    my_ccs811.reset()

    print(my_ccs811.read_byte(0x00))
    print(my_ccs811.read_byte(0x20))

    my_ccs811.start_app()

    my_ccs811.read_byte(0x00)
    measurement_time = time.time()

    while True:
        if my_ccs811.read_byte(0x00) == 152:
            my_ccs811.write_byte(0x02)
            data = my_ccs811.read_bytes(8)

            eco2 = data[0] << 8 | data[1]
            voc = data[2] << 8 | data[3]
            print(eco2, voc)

            if (time.time() - measurement_time) > 900:
                measurement_time = time.time()
                post_data([eco2, voc])
        else:
            if my_ccs811.read_byte(0x00) & 0x01:
                my_ccs811.close()
                my_ccs811 = CCS811()
                my_ccs811.reset()
                time.sleep(1)
                my_ccs811.start_app()
