import re
import os
import socket
import asyncio
import math
import errno
from struct import unpack
from functools import reduce
import sys
import time
import datetime


from basic_logtools.filelog import LogFile

from networktools.time import timestamp
from networktools.library import my_random_string
'''
###############################################################################
CLASE ERYO  __authors__ = " David Pineda"
###############################################################################
Conexion TCP/IP con un determinado receptor.
'''
from .eryo_settings import (ERYO_FIELD_NAMES, ERYO_REC, ERYO_TABLE_NAMES,
                            BUFF_MAX_SIZE, TABLES_SIZES, ERYO_LIST, SYNC_MARKER_VALUE, BLOCKS_FLAGS,
                            ETN_reverse, TABLES_BY_FLAG, CONS, MSG_ID, signal_check)

from networktools.colorprint import rprint, gprint, bprint
"""
Check verification

int eryo_trailer_decode(char *buf, int start, eryo_trailer_t *ptr)
{
  int index=start;
  DECODE_BITS(16, buf, index, ptr->checksum);
  assert(index - start==sizeof(eryo_trailer_t));
  return index;
}

inidice = partida
decodificar 2 bytes (16 bits) a variable checksu,
compara,  la diferencia (index-start) con tamaño de eryo_trailer_y


"""


def convert_data(key, table_name, data):
    size_table = ERYO_REC[table_name]
    field_names = ERYO_FIELD_NAMES[key]
    bytes_table = TABLES_SIZES[table_name]
    try:
        unpacked = unpack(size_table, data)
    except Exception as e:
        print("No unpack on converta data", e)
        raise e
    table_dict = dict(zip(field_names, unpacked))
    return table_dict


def checksum(data):
    check_data = list(data)
    suma = sum(check_data[:-2])
    return suma


class Eryo:
    """ Class to connect to tcp port and parse ERYO messages """
    tipo = "ERYO"

    def __init__(self, **kwargs):
        station = kwargs.get('code')
        sock = kwargs.get('sock')
        self.timeout = kwargs.get('timeout', 1)
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.sock = self.create_socket(None)
        self.loop = kwargs.get('loop')
        self.station = station
        self.sock.settimeout(self.timeout)
        self.msg_dict = {}
        self.msg_0 = None
        self.msg_bytes = None
        self.checksum = None
        self.rec_dict = {}
        self.batt_status = 0
        self.try_connect = 0
        self.id_columns = {}
        self.keys = []
        self.tables = ERYO_TABLE_NAMES
        self.status = False
        # log file for this station
        # create log instance
        log_path = kwargs.get('log_path', './logs')
        log_level = kwargs.get('log_level', 'INFO')
        self.logger = LogFile(self.class_name,
                              self.station,
                              self.host,
                              path=log_path,
                              base_level=log_level)
        # manage asyncronous clients
        self.logger.info("Log para %s" % self.station)
        self.idc = []
        self.clients = {}

    @property
    def class_name(self):
        return self.__class__.__name__

    def create_socket(self, sock):
        sock = None
        if sock is None:
            sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = sock
        return sock

    def off_blocking(self):
        self.sock.setblocking(False)

    def on_blocking(self):
        self.sock.setblocking(True)

    async def connect(self):
        host = self.host
        port = self.port
        loop = self.loop
        address = (host, port)
        while not self.status:
            try:
                (reader, writer) = await asyncio.open_connection(
                    loop=loop,
                    host=host,
                    port=port)
                idc = await self.set_reader_writer(reader, writer)
                if self.hard_beat(idc):
                    self.status = True
                    self.logger.info("Conexion a %s realizada" % self.station)
                else:
                    info = writer.get_extra_info('peername')
                    self.logger.error(info)
            except socket.timeout as timeout:
                self.on_blocking()
                self.logger.exception(
                    "Error en conexión con %s:%s, error: %s" % (host, port, timeout))
                #print("Error de socket a ERYO en conexión %s" % timeout)
                self.status = False
                await asyncio.sleep(10)
                # await self.connect()
                # raise timeout
            except socket.error as e:
                self.status = False
                self.on_blocking()
                if e.errno == errno.ECONNREFUSED:
                    # print("Conexión rechazada en %s" %
                    #      self.station, file=sys.stderr)
                    self.logger.exception(e)
                    await asyncio.sleep(10)
                else:
                    # print("No se puede establecer conexión, de %s" %
                    #      self.station, file=sys.stderr)
                    self.logger.exception(e)
                    await asyncio.sleep(10)
        return idc

    # callback for create server:

    def hard_beat(self, idc):
        if idc in self.clients:
            reader = self.clients[idc]['reader']
            writer = self.clients[idc]['writer']
            if writer.can_write_eof():
                return True
            else:
                self.logger.error("no hard_beat")
                self.close(idc)
                self.status = False
                return False
        else:
            self.logger.error("no hard_beat, idc %s not client" % idc)
            self.close(idc)
            self.status = False
            return False

    def info(self, idc):
        if self.clients:
            writer = self.clients[idc]['writer']
            return writer.get_extra_info('peername')
        else:
            return None

    def set_idc(self):
        """
        Defines a new id for relation process-collect_task, check if exists
        """
        uin = 4
        idc = my_random_string(uin)
        while True:
            if idc not in self.idc:
                self.idc.append(idc)
                break
            else:
                idc = my_random_string(uin)
        return idc

    async def set_reader_writer(self, reader, writer):
        idc = self.set_idc()
        # self.log_info_client(writer)
        self.clients.update(
            {idc: {
                'reader': reader,
                'writer': writer
            }
            }
        )
        return idc

    def list_clients(self):
        for i in range(len(self.conss)):
            print(str(self.addrs[i]) + ":" + str(self.conns[i]))

    def close(self, idc):
        self.logger.error("La conexión se cerró en cliente %s" % idc)
        self.status = False
        reader = self.clients[idc]['reader']
        writer = self.clients[idc]['writer']
        writer.close()

    def stop(self):
        for idc in self.clients:
            self.close(idc)

    async def get_records(self):
        """
        Obtener bytes y traducir a un msg ERYO

        """
        idc = self.select_idc
        reader = self.clients[idc]['reader']
        writer = self.clients[idc]['writer']
        sync_marker_first = SYNC_MARKER_VALUE.get('first')
        sync_marker_second = SYNC_MARKER_VALUE.get('second')
        t0 = time.time()
        try:
            if writer.transport.is_closing():
                self.logger.error("La conexión se cerró %s" % writer)
                self.status = False
                raise Exception("Conexión perdida")
            try:
                done = False
                counter = 1
                data = b''
                byte_a, byte_b = (0, 0)
                suma_bytes = 0
                msg = {}
                position = 0
                while not done:
                    byte_a = await reader.readexactly(1)
                    while byte_a != sync_marker_first:
                        byte_a = await reader.readexactly(1)
                    byte_b = await reader.readexactly(1)
                    if byte_b == sync_marker_second:
                        # read next 3 bytes
                        resto_header = await reader.readexactly(3)
                        suma_bytes += 5
                        header = byte_a+byte_b+resto_header
                        data += header
                        data_dict = convert_data(1, "ERYO_HEADER", header)
                        data_dict['MESSAGE_ID'] = MSG_ID.get(
                            data_dict.get("MESSAGE_ID"))
                        msg["ERYO_HEADER"] = data_dict
                        # POSITION_BLOCK
                        byte_count = data_dict.get("BYTE_COUNT")
                        all_bytes = await reader.readexactly(byte_count-5)
                        data += all_bytes
                        key_2 = "POSITION_BLOCK"
                        PB_bytes = TABLES_SIZES.get(key_2)
                        suma_bytes += PB_bytes
                        PB_data = all_bytes[position:position+PB_bytes]
                        position += PB_bytes
                        PB_dict = convert_data(2, key_2, PB_data)
                        SITE_ID = PB_dict["SITE_ID"].decode("utf8")
                        PB_dict["SITE_ID"] = re.sub("\x00+$", "", SITE_ID)
                        SOLUTION_ID = PB_dict["SOLUTION_ID"].decode("utf8")
                        PB_dict["SOLUTION_ID"] = re.sub(
                            "\x00+$", "", SOLUTION_ID)
                        msg["POSITION_BLOCK"] = PB_dict
                        FLAGS = PB_dict.get('FLAGS')
                        bloques = list(filter(
                            lambda e: e[1] > 0,
                            [(block, FLAGS & value) for block, value in
                             BLOCKS_FLAGS.items()]))
                        for block_name, value in bloques:
                            if block_name == 'SAT_INFO':
                                HDR = "SAT_HDR"
                                INFO = "SAT_INFO_BLOCK"
                                nbytes = TABLES_SIZES.get(HDR)
                                suma_bytes += nbytes
                                data_block = all_bytes[position:position+nbytes]
                                position += nbytes
                                n = ETN_reverse.get(HDR)
                                data_dict = convert_data(n, HDR, data_block)
                                msg["SAT_INFO"] = {HDR: data_dict}
                                msg["SAT_INFO"]["DATA"] = []
                                NRO_SATS = data_dict.get('SAT_BLOCK_COUNT')
                                key = TABLES_BY_FLAG.get("SAT_INFO")[1]
                                for i in range(NRO_SATS):
                                    nbytes = TABLES_SIZES.get(INFO)
                                    suma_bytes += nbytes
                                    data_block = all_bytes[position:position+nbytes]
                                    position += nbytes
                                    n = ETN_reverse.get(INFO)
                                    data_dict = convert_data(
                                        n, INFO, data_block)
                                    key = "CONSTELLATION"
                                    data_dict[key] = CONS.get(
                                        data_dict.get(key))
                                    key = "SIGNAL_FLAGS"
                                    data_dict["SIGNALS"] = signal_check(
                                        data_dict.get(key))
                                    msg["SAT_INFO"]["DATA"].append(data_dict)
                            else:
                                for key in TABLES_BY_FLAG.get(block_name):
                                    nbytes = TABLES_SIZES.get(key)
                                    suma_bytes += nbytes
                                    data_block = all_bytes[position:position+nbytes]
                                    position += nbytes
                                    n = ETN_reverse.get(key)
                                    data_dict = convert_data(
                                        n, key, data_block)
                                    msg[key] = data_dict
                        # CHECKSUM
                        key = "ERYO_TRAILER"
                        nbytes = TABLES_SIZES.get(key)
                        suma_bytes += nbytes
                        checksum_bytes = all_bytes[position:position+nbytes]
                        n = ETN_reverse.get(key)
                        # checksum_bytes = await reader.readexactly(nbytes)
                        data_dict = convert_data(n, key, checksum_bytes)
                        msg[key] = data_dict
                        checksum_msg = data_dict.get("CHECKSUM")
                        chsum = checksum(data)
                        done = checksum_msg == chsum
                return done, msg
            except socket.timeout as timeout:
                self.logger.warning(
                    "La conexión se cerró, socket timeout %s" % timeout)
                self.on_blocking()
                self.logger.exception()
                self.status = False
                await asyncio.sleep(.1)
                raise timeout
            except Exception as ex:
                self.logger.error(
                    "La conexión se cerró, error en comunicación %s" % ex)
                self.close(idc)
                self.on_blocking()
                info = "Error %s en estación %s. Encabezado con data %s" % (
                    ex, self.station, data)
                self.logger.info(info)
                self.logger.error(ex)
                self.status = False
                await asyncio.sleep(.1)
                if ex == socket.timeout:
                    self.sock = self.create_socket(None)
                    self.on_blocking()
                    await self.connect()
                raise ex
        except socket.timeout as timeout:
            self.logger.warning(
                "La conexión se cerró, socket timeout %s" % timeout)
            self.on_blocking()
            self.logger.exception()
            self.status = False
            await asyncio.sleep(.1)
            raise timeout
        except Exception as ex:
            self.logger.error(
                "La conexión se cerró, error en comunicación %s" % ex)
            self.close(idc)
            self.on_blocking()
            info = "Error %s en estación %s. Encabezado con data %s" % (
                ex, self.station, data)
            print(info)
            self.logger.info(info)
            self.logger.error(ex)
            self.status = False
            await asyncio.sleep(.1)
            if ex == socket.timeout:
                self.sock = self.create_socket(None)
                self.on_blocking()
                await self.connect()
            raise ex

    async def get_message_header(self, idc):
        self.select_idc = idc
