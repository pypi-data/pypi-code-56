#!/usr/bin/env python3
#
# Copyright 2020 Alexander Couzens <lynxis@fe80.eu>
# License: MIT

import struct

import usb.core
from usb.util import endpoint_address, endpoint_direction, ENDPOINT_IN, ENDPOINT_OUT, build_request_type, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE, CTRL_OUT, CTRL_IN

# in ms
TIMEOUT = 10

# all communication
BREQUEST_CPLD = 178
BREQUEST_DO = 183
BREQUEST_DEVICE_ID = 184
BREQUEST_COS = 185
BREQUEST_INITIAL = 187

COUNTER_TYPE_FREQUENCY = 0
COUNTER_TYPE_COUNTER = 1

COUNTER_TYPES = (COUNTER_TYPE_FREQUENCY, COUNTER_TYPE_COUNTER)

class DAQ7250():
    def __init__(self):
        self.dev = None
        self.connected = False

        # [input, output]
        self.interupt = [None, None]
        self.bulk = [None, None]

        # generic timeout in ms. Used for control timeout
        self.timeout = 100

        # irq timeout ins ms. When waiting for interrupts.
        self.irq_timeout = None

    def _search_by_deviceid(self, deviceid):
        for dev in usb.core.find(idVendor=0x144a, idProduct=0x7250, find_all=True):
            # this is a bit hacky, setting self.dev to use self.get_device_id
            self.dev = dev

            if self.get_device_id() == deviceid:
                return dev
        return None

    def connect(self, dev=None, deviceid=None):
        """
        Connects to the device.

        :params dev: If set, this device will be used instead of searched.
        :params deviceid: If set, the first device with this rotary id will be used.
        """
        if dev is None:
            if deviceid:
                dev = self._search_by_deviceid(deviceid)
            else:
                # use the first device
                dev = usb.core.find(idVendor=0x144a, idProduct=0x7250)

            if dev is None:
                raise ValueError('Device not found')

        self.dev = dev

        dev.set_configuration()
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]

        for endpoint in intf:
            if endpoint_address(endpoint.bEndpointAddress) == 0x1:
                if endpoint_direction(endpoint.bEndpointAddress) == ENDPOINT_IN:
                    self.interupt[0] = endpoint
                else:
                    self.interupt[1] = endpoint

            elif endpoint_address(endpoint.bEndpointAddress) == 0x6 \
                    and endpoint_direction(endpoint.bEndpointAddress) == ENDPOINT_IN:
                self.bulk[0] = endpoint
            elif endpoint_address(endpoint.bEndpointAddress) == 0x2 \
                    and endpoint_direction(endpoint.bEndpointAddress) == ENDPOINT_OUT:
                self.bulk[1] = endpoint

        if None in self.interupt:
            raise RuntimeError("Could not find interupt endpoint")

        if None in self.bulk:
            raise RuntimeError("Could not find bulk endpoint")

        self.connected = True

    def get_dos(self):
        """
        Retrieve the Digital Output state from the device.

        :returns: A bit mask. Each bit represents a single line.
        """
        bmreq = build_request_type(CTRL_IN, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        transfer = self.dev.ctrl_transfer(
            bmreq, BREQUEST_DO,
            wValue=0x4, wIndex=0,
            data_or_wLength=1, timeout=self.timeout)
        return transfer[0]

    def set_dos(self, lines):
        """
        Set the Digital Outputs.

        :param lines: A bit mask describing the new state.
        """

        if lines < 0 or lines > 0xff:
            raise RuntimeError("Invalid Value for lines. lines must be 8 bit")

        # there is only one port with 8 lines
        bmreq = build_request_type(CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_DO,
            wValue=0xff03, wIndex=lines,
            data_or_wLength=[], timeout=self.timeout)

    def get_dos_initial(self):
        """
        Get the initial Digital Output state after power up.

        :returns: A bit msak. Each bit represents a single line.
        """
        bmreq = build_request_type(CTRL_IN, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        transfer = self.dev.ctrl_transfer(
            bmreq, BREQUEST_INITIAL,
            wValue=0xd028, wIndex=0,
            data_or_wLength=2, timeout=self.timeout)

        return struct.unpack('<H', transfer[0:2])[0]

    def set_dos_initial(self, lines):
        """
        Set the initial Digital Output state after power up.

        :params lines: A bit msak. Each bit represents a single line.
        """

        if lines < 0 or lines > 0xff:
            raise RuntimeError("Invalid Value for lines. lines must be 8 bit")

        bmreq = build_request_type(CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_INITIAL,
            wValue=0xd028, wIndex=lines,
            data_or_wLength=[], timeout=self.timeout)

    def get_dis(self):
        """
        Read the state of all Digital Inputs

        :returns: A bit mask. Each bit represents a single line.
        """

        bmreq = build_request_type(CTRL_IN, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        transfer = self.dev.ctrl_transfer(
            bmreq, BREQUEST_CPLD,
            wValue=0xd00a, wIndex=0,
            data_or_wLength=1, timeout=self.timeout)
        return transfer[0]

    def set_di_min_pulse_width(self, pulse):
        """
        Set the minimum pulse width for the digital filter.
        The CPLD can filter digital inputs to ensure a level change last at least some time.
        The pulse width length can be only set for all inputs, but it can be enabled or disabled
        for each line indivitual.

        :params pulse: Define the pulse width in 1/48Mhz steps (16 bit).
        """

        value = struct.pack('<H', pulse)

        bmreq = build_request_type(CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_CPLD,
            wValue=0xd00c, wIndex=0,
            data_or_wLength=value, timeout=self.timeout)

    def set_di_digital_filter(self, lines):
        """
        Enable minimum pulse width filter on specific Digital Inputs.

        See set_di_min_pulse_width for further information on the digital filter.

        :params lines: The DI lines as bit mask.
        """

        if lines < 0 or lines > 0xff:
            raise RuntimeError("Invalid Value for lines. lines must be 8 bit")

        bmreq = build_request_type(CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_CPLD,
            wValue=0xd00c, wIndex=0,
            data_or_wLength=[lines], timeout=self.timeout)

    def set_di_cos(self, lines):
        """
        Enable COS IRQ on specific Digital Input lines.
        COS (change of state) IRQ can be enabled on each Digital Input line.

        :params lines: The DI lines as bit mask.
        """

        if lines < 0 or lines > 0xff:
            raise RuntimeError("Lines is not a 8 bit bitmask")

        # enable interrupt on the CPLD
        bmreq = build_request_type(CTRL_IN, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_CPLD,
            wValue=0xd000, wIndex=0,
            data_or_wLength=[lines], timeout=self.timeout)

        # maybe clear interrupt?
        bmreq = build_request_type(CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_COS,
            wValue=0x00, wIndex=0x00,
            data_or_wLength=[], timeout=self.timeout)

    def wait_di_cos_irq(self):
        """
        Wait for a COS IRQ. Returns when the IRQ fired.

        :returns: The values from the IRQ.
        """
        transfer = self.interupt[0].read(4, self.irq_timeout)

        # e.g. [ 0x80, 0x00, 0x80, 0x00 ] when pin 8 changed.
        return transfer

    def get_counter_edge(self, counter):
        """
        Retrieve the counter value.
        The counting edge can be defined via set_counter() polarity.

        :returns: The counter value.
        """

        return self.get_counter(counter, ctype=COUNTER_TYPE_COUNTER)

    def get_counter_freq(self, counter):
        """
        Retrieve the frequency of a counter.

        :returns: The counter frequency in Hz as float.
        """

        clk_length_20ns = self.get_counter(counter, ctype=COUNTER_TYPE_FREQUENCY)
        freq = 1 / (clk_length_20ns * 20e-09)
        return freq

    def get_counter_period_raw(self, counter):
        """
        Retrieve the clock period of a counter.
        The 7250 protocol is using 1/48Mhz steps.

        :returns: The clock period in 1/48Mhz step.
        """
        return self.get_counter(counter, ctype=COUNTER_TYPE_FREQUENCY)

    def get_counter_period_raw(self, counter):
        """
        Retrieve the clock period of a counter.
        The 7250 protocol is using 20ns steps.

        :returns: The clock period in ns
        """

        clk_period = self.get_counter(counter, ctype=COUNTER_TYPE_FREQUENCY)
        return clk_period / 48e6

    def get_counter(self, counter, ctype=COUNTER_TYPE_COUNTER):
        """
        Return the counter frequency of a counter.

        :param ctype: The type of the counter. COUNTER_TYPE_FREQUENCY or COUNTER_TYPE_COUNTER
        :param counter: The counter to retrieve. 0 or 1.
        :returns: Depending on ctype a count or 20ns clock period.
        """

        wValue = 0xd000

        if ctype == COUNTER_TYPE_FREQUENCY:
            wValue |= 0x18
        elif ctype == COUNTER_TYPE_COUNTER:
            wValue |= 0x20
        else:
            raise RuntimeError("Unknown counter type!")

        # bit 3 define which counter
        if counter == 0:
            wValue |= 0x4
        elif counter == 1:
            wValue |= 0x0
        else:
            raise RuntimeError("Argument counter is out of range. counter must be 0-1")

        bmreq = build_request_type(CTRL_IN, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        transfer = self.dev.ctrl_transfer(
            bmreq, BREQUEST_CPLD,
            wValue, wIndex=0,
            data_or_wLength=4, timeout=self.timeout)

        # counter:
        # 5263
        # [ 0x8f, 0x14, 0x00, 0x00 ]

        # freq:
        # 9.647365 Hz.
        # [ 0x5c, 0xeb, 0x4b, 0x00 ]

        # freq:
        # 968.054199 Hz.
        # [ 0xb0, 0xc1, 0x00, 0x00 ]

        return struct.unpack('<I', transfer[0:4])[0]

    def set_counter(self,
                    counter,
                    counter_filter=False,
                    polarity=False,
                    reset_frequency_counter=False,
                    reset_edge_counter=False):
        """
        Change counter properties or reset the counter or frequenct value.

        :params counter_filter: Enable digital input filter.
        :params polarity: Set polarity to high (True) or low (False)
        :params reset_frequency_counter: Reset the frequency counter.
        :params reset_edge_counter: Reset the edge counter.
        """

        wValue = 0xd010

        # bit 3 define which counter
        if counter == 0:
            wValue |= 0x4
        elif counter == 1:
            wValue |= 0x0
        else:
            raise RuntimeError("Argument counter is out of range. counter must be 0-1")

        value = 0

        if counter_filter:
            value |= 0x1

        if reset_edge_counter:
            value |= 0x2

        if reset_frequency_counter:
            value |= 0x4

        if polarity:
            value |= 0x8

        bmreq = build_request_type(CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_CPLD,
            wValue, wIndex=0x00,
            data_or_wLength=[value, 0x00, 0x00, 0x00], timeout=self.timeout)

    def set_counter_min_pulse_width(self, counter, pulse):
        """
        :params counter: Define which counter should work.
        :params pulse: Define the pulse width in 1/48Mhz steps (16 bit).
        """

        value = struct.pack('<H', pulse)

        wValue = 0xd028

        # bit 3 define which counter
        if counter == 0:
            wValue |= 0x4
        elif counter == 1:
            wValue |= 0x0
        else:
            raise RuntimeError("Argument counter is out of range. counter must be 0-1")

        bmreq = build_request_type(CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        self.dev.ctrl_transfer(
            bmreq, BREQUEST_CPLD,
            wValue, wIndex=0,
            data_or_wLength=value, timeout=self.timeout)

    def get_device_id(self):
        """
        Read the device id, which can be set via a rotary switch.

        :returns: device id (0-7)
        """

        bmreq = build_request_type(CTRL_IN, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE)
        transfer = self.dev.ctrl_transfer(
            bmreq, BREQUEST_DEVICE_ID,
            0x4, wIndex=0,
            data_or_wLength=1, timeout=self.timeout)
        return transfer[0]

if __name__ == "__main__":
    DAQ = DAQ7250()
    DAQ.connect()
    print(DAQ.get_counter_edge(1))
