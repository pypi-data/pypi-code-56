from struct import unpack
import socket
import asyncio
import math
import errno
from functools import reduce

import sys
import time
import datetime

from pathlib import Path
import os
from basic_logtools.filelog import LogFile

from networktools.time import timestamp, now
from networktools.library import my_random_string

from networktools.colorprint import rprint, bprint

'''
###############################################################################
CLASE GSOF  __authors__ = "Henry T. Berglund ----> David Pineda"
###############################################################################
Conexion TCP/IP con un determinado receptor.
Updated to python3.5 by David Pineda @pineiden dpineda@csn.uchile.cl

'''

try:
    from .gsof_settings import gsof_field_names, gsof_rec, gsof_table_names, logfile
except Exception:
    from gsof_settings import gsof_field_names, gsof_rec, gsof_table_names, logfile

def checksum256(data_check):
    """Calculate checksum"""
    # ord: string -> unicode int
    # map(a,b): opera a en b
    # list entrega lista o arrays
     #formula: 	(Status + type + length + data bytes) modulo 256
    data_bytes = data_check.get("DATA_BYTES")
    checksum = data_check.get("CHECKSUM")
    chk256  = sum(data_bytes) % 256
    return  checksum == chk256

class Gsof:
    """ Class to connect to tcp port and parse GSOF messages """
    tipo = "GSOF"

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
        self.tables = gsof_table_names
        self.status = False

        # manage asyncronous clients
        self.idc = []
        self.clients = {}
        log_path = kwargs.get('log_path', './logs')
        log_level = kwargs.get('log_level', 'INFO')
        self.logger = LogFile(self.class_name,
                              station,
                              self.host,
                              path=log_path,
                              base_level=log_level)
        # manage asyncronous clients
        self.logger.info("Log para %s" % self.station)

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
                if self.heart_beat(idc):
                    self.status = True
                    self.logger.info("Conexion a %s realizada" % self.station)
                else:
                    info = writer.get_extra_info('peername')
                    self.logger.error(info)
            except socket.timeout as timeout:
                self.on_blocking()
                self.logger.error(
                    "Error en conexión con %s:%s, error: %s" % (host, port, timeout))
                #print("Error de socket a GSOF en conexión %s" % timeout)
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
                    self.logger.exception("Error al conectar %s, station %s" %(e, self.station))
                    await asyncio.sleep(10)
                else:
                    # print("No se puede establecer conexión, de %s" %
                    #      self.station, file=sys.stderr)
                    self.logger.exception("Otro tipo de error al conectar %s, station %s" %(e, self.station))
                    await asyncio.sleep(10)

            await asyncio.sleep(.2)

        return idc

    # callback for create server:

    def heart_beat(self, idc):
        tnow = now()
        if idc in self.clients.keys():
            reader = self.clients[idc]['reader']
            writer = self.clients[idc]['writer']
            closing = writer.is_closing()
            extra_info = writer.get_extra_info('peername')
            at_eof = reader.at_eof()
            if not closing and extra_info and not at_eof:
                return True
            else:
                print("Fail heart beat to %s, at %s" %(self.station, tnow))
                msg_error = "Closing %s, extra_info %s, at_eof %s" %(closing, extra_info,at_eof)
                print(msg_error)
                self.logger.error(msg_error)
                self.logger.error("no heart_beat, at %s" %tnow)
                self.close(idc)
                self.status = False
                return False
        else:
            self.logger.error("no heart_beat, idc %s not client, code station %s" % (idc, self.station))
            self.close(idc)
            self.status = False
            return False
 
    def info(self, idc):
        if self.clients:
            writer = self.clients[idc]['writer']
            return idc, writer.get_extra_info('peername')
        else:
            return idc, None

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

    async def close(self, idc):
        self.logger.error("La conexión se cerró en cliente %s" % idc)
        self.status = False
        reader = self.clients[idc]['reader']
        writer = self.clients[idc]['writer']
        writer.close()
        await writer.wait_closed()

    async def stop(self):
        for idc in self.clients:
            await self.close(idc)

    async def get_message_header(self, idc):
        # receive data from source
        # max amount of data
        # N ammount of bites
        self.data_check = {}
        reader = self.clients[idc]['reader']
        writer = self.clients[idc]['writer']
        self.timestamp = timestamp()
        BytesData = 7
        bufsize = BytesData
        msg_field_names = ('STX', 'STATUS', 'TYPE', 'LENGTH',
                           'T_NUM', 'PAGE_INDEX', 'MAX_PAGE_INDEX')

        try:
            if writer.transport.is_closing():
                self.logger.error("La conexión se cerró %s" % writer)
                self.status = False
                raise Exception("Conexión perdida para idc %s station %s" %(idc, self.station))
            data = None

            try:
                data = await reader.readexactly(bufsize)
                self.msg_dict = dict(zip(
                    msg_field_names,
                    unpack('>' + str(bufsize) + 'B', data)))
                campos_unpack =unpack('>%dB'%bufsize, data)
                self.msg_dict = dict(zip(msg_field_names, campos_unpack))
                status = self.msg_dict['STATUS']
                bin_status = bin(status)
                batt_status = bin_status[3]
                self.msg_dict["LOW_BATTERY"] = bool(int(batt_status))
                self.msg_bytes = await reader.readexactly(self.msg_dict['LENGTH']-3)
                self.msg_0 = self.msg_bytes                
                check_etx =  await reader.readexactly(n=2)
                (checksum, etx) = unpack('>2B', check_etx)
                self.data_check["CHECKSUM"] = checksum                
                self.data_check["DATA_BYTES"] = list(self.msg_bytes+data[1:])
                self.checksum = checksum256(self.data_check)
                self.msg_dict["CHECKED"] = self.checksum
            except socket.timeout as timeout:
                self.logger.exception(
                    "La conexión se cerró, socket timeout %s, STATION %S" % (timeout, self.station))
                self.on_blocking()
                self.logger.exception("Esperando mucho tiempo")
                self.status = False
                raise timeout
            except Exception as ex:
                self.logger.exception(
                    "La conexión se cerró, error en comunicación %s" % ex)
                self.close(idc)
                self.on_blocking()
                info = "Error %s en estación %s. Encabezado con data %s" % (
                    ex, self.station, data)
                print(info)
                self.logger.info(info)
                self.logger.error(ex)
                self.status = False
                raise ex

        except asyncio.IncompleteReadError as e:
            self.logger.exception("Error de mensaje incompleto %s" % e)
            self.logger.error(
                "Error de mensaje esperado en n bytes %s" % e.expected)
            self.logger.error("Error de mensaje recibido %s" % e.partial)
            raise e

        except socket.timeout:
            self.close()
            self.sock = self.create_socket(None)
            self.on_blocking()
            raise socket.timeout

        except socket.error as ex:
            self.close()
            print("Error de conexión %s error %s" % (self.station, ex))
            self.logger.error(ex)
            self.sock = self.create_socket(None)
            self.on_blocking()
            raise ex

    async def get_records(self):
        msg = {}        
        while self.msg_bytes:
            # READ THE FIRST TWO BYTES FROM RECORD HEADER
            try:
                record_type, record_length = unpack('>2B', self.msg_bytes[0:2])
            except Exception as ex:
                self.status = False
                qex = "Error %s en estación %s, tabla %s" % (
                    ex, self.station, 'Header')
                self.logger.debug(qex)
                if ex == socket.timeout:
                    self.on_blocking()
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.connect())

            self.msg_bytes = self.msg_bytes[2:]
            try:
                msg_table = self.select_record(record_type, record_length)
                msg.update(msg_table)
            except Exception as ex:
                self.status = False
                self.logger.error(ex)
                print("No hay mensaje que traducir")
                self.logger.error("Desconectando debido a error en mensaje")
                self.logger.error(
                    "Reconectando debido a error en mensaje, luego de desconexión")
                self.on_blocking()
                return False, {}
        msg["HEADER"] = self.msg_dict
        done = self.checksum
        return done, msg

    def select_record(self, record_type, record_length):
        field_names = gsof_field_names
        rec_input = gsof_rec
        msg = []
        table_name = self.tables.get(record_type)
        timestamp = self.timestamp
        try:
            rec_field_names = field_names.get(record_type)
            if not record_type in [13, 14, 33, 48] and record_type in field_names.keys():
                # print("Base recibida")
                try:
                    rec_values = unpack(
                        rec_input[record_type], self.msg_bytes[:record_length])
                    msg = dict(list(zip(rec_field_names, rec_values)))
                    msg['TIMESTAMP'] = timestamp
                    self.rec_dict.update({table_name: msg})
                    self.msg_bytes = self.msg_bytes[record_length:]
                except Exception as ex:
                    self.status = False
                    self.logger.exception("Error al hacer unpack",ex)
                    raise ex

            elif record_type in [13, 14, 33, 48] and record_type in field_names.keys():
                L = len(self.msg_bytes)-1
                bNUM = self.msg_bytes[0:1]
                try:
                    code = rec_input[record_type][0]
                    NUM_OF_SVS = unpack(code, bNUM)  # char-> pass to int
                except Exception as ex:
                    self.status = False
                    qex = "Error %s en estación %s, tabla %s" % (
                        ex, self.station, record_type)
                    self.logger.exception(qex)
                    raise ex
                u = int(L/NUM_OF_SVS[0])
                # Acortar el NSVS quitando primer byte
                self.msg_bytes = self.msg_bytes[1:]
                # for field in range(len(rec_field_names)):
                #    self.rec_dict[rec_field_names[field]] = []
                for sat in range(NUM_OF_SVS[0]):
                    try:
                        code = rec_input[record_type][1]
                        rec_values = unpack(
                            code, self.msg_bytes[0:u])  # why [0:10]
                        msg_k = dict(list(zip(rec_field_names, rec_values)))
                        msg_k['TIMESTAMP'] = timestamp
                        msg.append(msg_k)
                    except Exception as ex:
                        self.status = False
                        self.logger.debug(ex)
                        raise ex
                    self.msg_bytes = self.msg_bytes[u:]
                    tname = table_name+"_"+str(sat)
                    self.rec_dict.update({table_name: msg})
            else:
                """Unknown record type? Skip it for now!"""
                # print record_type
                msg = self.msg_bytes[record_length + 2:]
                self.msg_bytes = self.msg_bytes[record_length + 2:]
        except Exception as ex:
            self.status = False
            raise ex
        return {table_name: msg}


