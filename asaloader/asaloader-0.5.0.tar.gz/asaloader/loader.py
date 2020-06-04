# -*- coding: utf-8 -*-
import argparse
import enum
import math
import os
import time

import serial
import progressbar

from asaloader import alp
from asaloader import ihex

from asaloader.device import device_list
from asaloader.locale import _
from asaloader import exceptions

class CommandTrnasHandler():
    def __init__(self, ser):
        self._ser = ser
        self._pd = alp.Decoder()
        self.timeout = 5

    def _get_packet(self):
        start_time = time.clock()
        exec_time = 0
        exit_flag = False
        pac_decode_err_flag = False
        packet = None

        while exec_time < 3 and exit_flag is False:
            ch = self._ser.read(1)

            if len(ch) != 0:
                self._pd.step(ch[0])

            if self._pd.isDone():
                packet = self._pd.getPacket()
                exit_flag = True
            elif self._pd.isError():
                pac_decode_err_flag = True
                exit_flag = True
            exec_time = time.clock() - start_time

        if exec_time > self.timeout:
            # timeout error
            # TODO exception
            raise exceptions.ComuError

        if pac_decode_err_flag:
            # packet decode error
            raise exceptions.ComuError

        return packet

    def _put_packet(self, cmd, data):
        req_raw = alp.encode(cmd, data)
        self._ser.write(req_raw)


    def cmd_chk_protocol(self):
        self._put_packet(alp.Command.CHK_PROTOCOL, b'test')
        rep = self._get_packet()

        if rep == None:
            return False, 0
        if rep['command'] == alp.Command.ACK1 and rep['data'] == b'OK!!':
            return True, 1
        elif rep['command'] == alp.Command.CHK_PROTOCOL and rep['data'][0] == 0:
            return True, rep['data'][1]
        else:
            return False, 0

    # commands for v1
    def cmd_v1_enter_prog(self):
        res, version = self.cmd_chk_protocol()
        if res and version == 1:
            return True

    def cmd_v1_flash_write(self, page_data):
        # v1 寫入 flash 不會有回應，且下次寫入需要等待 0.03 s
        self._put_packet(alp.Command.DATA, page_data)
        return True
    
    def cmd_v1_prog_end(self):
        self._put_packet(alp.Command.DATA, b'')
        rep = self._get_packet()

        if rep['command'] == alp.Command.ACK2 and rep['data'] == b'OK!!':
            return True
        else:
            return False

    # commands for v2
    def cmd_v2_enter_prog(self):
        res, version = self.cmd_chk_protocol()
        if res and version == 2:
            return True

    def cmd_v2_prog_chk_device(self):
        self._put_packet(alp.Command.PROG_CHK_DEVICE, b'')
        rep = self._get_packet()

        if rep['command'] == alp.Command.PROG_CHK_DEVICE and rep['data'][0] == 0:
            return True, rep['data'][1]
        else:
            return False

    def cmd_v2_prog_end(self):
        self._put_packet(alp.Command.PROG_END, b'')
        rep = self._get_packet()

        if rep['command'] == alp.Command.PROG_END and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_prog_end_and_go_app(self):
        self._put_packet(alp.Command.PROG_END_AND_GO_APP, b'')
        rep = self._get_packet()

        if rep['command'] == alp.Command.PROG_END_AND_GO_APP and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_prog_set_go_app_delay(self, t):
        self._put_packet(alp.Command.PROG_SET_GO_APP_DELAY, t.to_bytes(2, 'little'))
        rep = self._get_packet()

        if rep['command'] == alp.Command.PROG_SET_GO_APP_DELAY and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_flash_set_pgsz(self, size):
        self._put_packet(alp.Command.FLASH_SET_PGSZ, size.to_bytes(4, 'little'))
        rep = self._get_packet()
        if rep['command'] == alp.Command.FLASH_SET_PGSZ and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_flash_get_pgsz(self):
        self._put_packet(alp.Command.FLASH_GET_PGSZ, b'')
        rep = self._get_packet()
        if rep['command'] == alp.Command.FLASH_GET_PGSZ and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:3], 'little')
        else:
            return False

    def cmd_v2_flash_write(self, page_addr, data):
        paylod = page_addr.to_bytes(4, 'little') + data
        self._put_packet(alp.Command.FLASH_WRITE, paylod)
        rep = self._get_packet()
        if rep['command'] == alp.Command.FLASH_WRITE and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_flash_read(self):
        self._put_packet(alp.Command.FLASH_READ, b'')
        rep = self._get_packet()
        if rep['command'] == alp.Command.FLASH_READ and rep['data'][0] == 0:
            return True, rep['data']
        else:
            return False

    def cmd_v2_flash_earse_sector(self, num):
        self._put_packet(alp.Command.FLASH_EARSE_SECTOR, num.to_bytes(2, 'little'))
        rep = self._get_packet()
        if rep['command'] == alp.Command.FLASH_EARSE_SECTOR and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_flash_earse_all(self):
        self._put_packet(alp.Command.FLASH_EARSE_ALL, b'')
        rep = self._get_packet()
        if rep['command'] == alp.Command.FLASH_EARSE_ALL and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_eep_set_pgsz(self, size):
        self._put_packet(alp.Command.EEPROM_SET_PGSZ,
                         size.to_bytes(4, 'little'))
        rep = self._get_packet()
        if rep['command'] == alp.Command.EEPROM_SET_PGSZ and rep['data'][0] == 0:
            return True
        else:
            return False

    def cmd_v2_eep_get_pgsz(self):
        self._put_packet(alp.Command.EEPROM_GET_PGSZ, b'')
        rep = self._get_packet()
        if rep['command'] == alp.Command.EEPROM_GET_PGSZ and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:3], 'little')
        else:
            return False

    def cmd_v2_eep_write(self, page_data):
        self._put_packet(alp.Command.EEPROM_WRITE, page_data)
        rep = self._get_packet()
        if rep['command'] == alp.Command.EEPROM_WRITE and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_eep_read(self):
        self._put_packet(alp.Command.EEPROM_READ, b'')
        rep = self._get_packet()
        if rep['command'] == alp.Command.EEPROM_READ and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_eep_earse(self):
        self._put_packet(alp.Command.EEPROM_EARSE, b'')
        rep = self._get_packet()
        if rep['command'] == alp.Command.EEPROM_EARSE and rep['data'][0] == 0:
            return True, int.from_bytes(rep['data'][1:5], 'little')
        else:
            return False

    def cmd_v2_eep_earse_all(self):
        self._put_packet(alp.Command.EEPROM_EARSE_ALL, b'')

        rep = self._get_packet()
        if rep['command'] == alp.Command.EEPROM_EARSE_ALL and rep['data'][0] == 0:
            return True
        else:
            return False


class Loader():
    _device_type = int()

    _is_flash_prog = bool()
    _is_eeprom_prog = bool()
    _is_go_app = bool()

    _flash_file = str()
    _eep_file = str()
    _go_app_delay = int()

    class _Stage(enum.IntEnum):
        PREPARE   = 0
        FLASH_PROG = 1
        EEP_PROG = 2
        END = 3
    
    _stage = _Stage(_Stage.PREPARE)
    _stage_iter = None

    _total_steps = 0
    _cur_step = 0

    _flash_pages = list()
    _eep_pages = list()
    _flash_page_idx = int()
    _eep_page_idx = int()

    # output info
    _flash_size = int(0)
    _eep_size = int(0)
    _prog_time = float(0)

    def __init__(
            self,
            ser: serial.Serial,
            device_type: int = 0,
            is_flash_prog: bool = False,
            is_eeprom_prog: bool = False,
            is_go_app: bool = False,
            flash_file: str = '',
            eeprom_file: str = '',
            go_app_delay: int = 0,
        ):
        self._ser = ser

        self._cth = CommandTrnasHandler(ser)

        self._device_type = device_type
        self._is_flash_prog = is_flash_prog
        self._is_eeprom_prog = is_eeprom_prog
        self._is_go_app = is_go_app
        self._flash_file = flash_file
        self._eep_file = eeprom_file
        self._go_app_delay = go_app_delay

        self._prepare()

        self._prog_time
    
    @property
    def stage(self):
        return self._stage
    
    @property
    def device_type(self):
        return self._device_type
    
    @property
    def total_steps(self):
        return self._total_steps
    
    @property
    def flash_size(self):
        return self._flash_size

    @property
    def eeprom_size(self):
        return self._eep_size

    @property
    def prog_time(self):
        return self._prog_time

    def _prepare(self):
        if self._device_type > len(device_list):
            raise exceptions.DeviceTypeError(self._device_type)

        if self._is_flash_prog:
            if os.path.isfile(self._flash_file) is False:
                raise FileNotFoundError
        
        if self._is_eeprom_prog:
            if os.path.isfile(self._eep_file) is False:
                raise FileNotFoundError

        if self._is_go_app:
            if self._go_app_delay > 65535:
                raise exceptions.GoAppDelayValueError(self._go_app_delay)
        
        self._prepare_flash()
        self._prepare_eeprom()
        self._prepare_device()
        
        ## Stage
        stg_list = list()
        if self._is_flash_prog:
            stg_list.append(self._Stage.FLASH_PROG)
            self._total_steps += len(self._flash_pages)
        if self._is_eeprom_prog:
            stg_list.append(self._Stage.EEP_PROG)
            self._total_steps += len(self._eep_pages)
        stg_list.append(self._Stage.END)
        self._total_steps += 1
        self._stage_iter = iter(stg_list)
        self._stage = next(self._stage_iter)

        ## prog time
        if self._device_type == 1 or self._device_type == 2:
            self._prog_time = len(self._flash_pages) * 0.047 + len(self._eep_pages) * 0.05 + 0.23
        elif self._device_type == 3:
            # asa_m128_v2
            self._prog_time = len(self._flash_pages) * 0.047 + len(self._eep_pages) * 0.05 + 0.23
        elif self._device_type == 4:
            # asa_m3_v1
            self._prog_time = len(self._flash_pages) * 0.5 + len(self._eep_pages) * 0.05 + 0.23

    
    def _prepare_device(self):
        """檢查裝置是否吻合設定的裝置號碼
        
        Raises:
            exceptions.ComuError: 無法通訊
            exceptions.CheckDeviceError: 裝置比對錯誤
        """
        res, ver = self._cth.cmd_chk_protocol()

        if res and ver == 1:
            # protocol v1 dosn't have "chk_device" command
            # m128_v1 or m128_v2
            # use m128_v2 for default
            detected_device = 2
        elif res and ver == 2:
            res2, detected_device = self._cth.cmd_v2_prog_chk_device()
            if res2 is False:
                raise exceptions.ComuError()
        else:
            raise exceptions.ComuError()

        # auto detect device
        if device_list[self._device_type]['protocol_version'] == 0:
            self._device_type = detected_device
        
        # check for protocol v1 (e.g. m128_v1, m128_v2)
        elif device_list[self._device_type]['protocol_version'] == 1:
            if self._device_type != 2 or self._device_type != 1:
                raise exceptions.CheckDeviceError(self._device_type, detected_device)

        # check for protocol v2 (e.g. m128_v3, m3_v1)
        elif device_list[self._device_type]['protocol_version'] == 2:
            if detected_device != self._device_type:
                raise exceptions.CheckDeviceError(self._device_type, detected_device)

        self._protocol_version = device_list[self._device_type]['protocol_version']
    
    def _prepare_flash(self):
        if self._is_flash_prog:
            try:
                blocks = ihex.parse(self._flash_file)
                self._flash_size = sum([len(block['data']) for block in blocks])
                blocks = ihex.padding_space(blocks, 256, 0xFF)
                self._flash_pages = ihex.cut_to_pages(blocks, 256)
            except Exception:
                raise exceptions.FlashIsNotIhexError(self._flash_file)

    def _prepare_eeprom(self):
        if self._is_eeprom_prog:
            try:
                blocks = ihex.parse(self._eep_file)
                self._eeprom_size = sum([len(block['data']) for block in blocks])
                blocks = ihex.padding_space(blocks, 256, 0xFF)
                self._eeprom_pages = ihex.cut_to_pages(blocks, 256)
            except Exception:
                raise exceptions.EepromIsNotIhexError(self._eep_file)

    def _do_flash_prog_step(self):
        address = self._flash_pages[self._flash_page_idx]['address']
        data    = self._flash_pages[self._flash_page_idx]['data']
        if self._protocol_version == 1:
            # protocol v1 will auto clear flash after command "chk_protocol"
            self._cth.cmd_v1_flash_write(data)
            time.sleep(0.03)
        elif self._protocol_version == 2:
            if self._flash_page_idx == 0:
                self._cth.cmd_v2_flash_earse_all()
            self._cth.cmd_v2_flash_write(address, data)
        
        self._flash_page_idx += 1
        self._cur_step += 1

        if self._flash_page_idx == len(self._flash_pages):
            self._stage = next(self._stage_iter)

    def _do_eep_prog_step(self):
        if self._protocol_version == 2:
            self._cth.cmd_v2_eep_write(self._eep_pages[self._eep_page_idx])

        self._eep_page_idx += 1
        self._cur_step += 1
        if self._eep_page_idx == len(self._eep_pages):
            self._stage = next(self._stage_iter)

    def _do_prog_end_step(self):
        if self._protocol_version == 1:
            self._cth.cmd_v1_prog_end()
        elif self._protocol_version == 2:
            if self._is_go_app:
                self._cth.cmd_v2_prog_set_go_app_delay(self._go_app_delay)
                self._cth.cmd_v2_prog_end_and_go_app()
            else:
                self._cth.cmd_v2_prog_end()
        self._cur_step += 1

    def do_step(self):
        if self.stage == self._Stage.FLASH_PROG:
            self._do_flash_prog_step()
        elif self.stage == self._Stage.EEP_PROG:
            self._do_eep_prog_step()
        elif self.stage == self._Stage.END:
            self._do_prog_end_step()
