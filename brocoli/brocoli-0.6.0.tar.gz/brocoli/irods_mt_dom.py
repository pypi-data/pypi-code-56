from six import print_

import os

import socket
import struct
import threading
from concurrent.futures import ThreadPoolExecutor

import M2Crypto


from irods.manager.data_object_manager import DataObjectManager

from irods.message import (
    iRODSMessage, FileOpenRequest, ObjCopyRequest, StringStringMap, DataObjInfo, ModDataObjMeta, Message, IntegerProperty, StringProperty, SubmessageProperty)

#define PortList_PI "int portNum; int cookie; int sock; int windowSize;
# str hostAddr[LONG_NAME_LEN];"


class PortList(Message):
    _name = 'PortList_PI'
    portNum = IntegerProperty()
    cookie = IntegerProperty()
    sock = IntegerProperty()
    windowSize = IntegerProperty()
    hostAddr = StringProperty()


# define PortalOprOut_PI "int status; int l1descInx; int numThreads;
# str chksum[NAME_LEN]; struct PortList_PI;"


class PortalOprResponse(Message):
    _name = 'PortalOprOut_PI'
    status = IntegerProperty()
    l1descInx = IntegerProperty()
    numThreads = IntegerProperty()
    chksum = StringProperty()
    PortList_PI = SubmessageProperty(PortList)

# define INT_PI "int myInt;"


class OprComplete(Message):
    _name = 'INT_PI'
    myInt = IntegerProperty()


import irods.exception as ex
from irods.api_number import api_number
from irods import DEFAULT_CONNECTION_TIMEOUT
import irods.keywords as kw

class LockCounter:
    def __init__(self, value=0):
        self.lock = threading.Lock()
        self.__value = value

    def __get_value(self):
        return self.__value

    def __set_value(self, new_value):
        with self.lock:
            self.__value = new_value
            return self.__value

    value = property(__get_value, __set_value)

    def __add(self, add):
        with self.lock:
            self.__value += add
            return self.__value

    def incr(self, increment=1):
        return self.__add(increment)

    def decr(self, decrement=1):
        return self.__add(- decrement)

def connect_to_portal(host, port, cookie,
                      timeout=DEFAULT_CONNECTION_TIMEOUT):
    address = (host, port)
    try:
        s = socket.create_connection(address, timeout)
    except socket.error:
        raise ex.NetworkException(
            "Could not connect to specified host and port: " +
            "{}:{}".format(*address))

    fmt = '!i'
    sent = s.send(struct.pack(fmt, cookie))

    if sent != struct.calcsize(fmt):
        s.close()
        raise ex.NetworkException(
            "SYS_PORT_COOKIE_ERR: {}:{}".format(*address))

    return s

def recv_xfer_header(sock):
    # typedef struct TransferHeader { int oprType; int flags;
    # rodsLong_t offset; rodsLong_t length; } transferHeader_t;

    fmt = '!iiqq'
    size = struct.calcsize(fmt)
    buf = bytearray(size)
    recv_size = sock.recv_into(buf, size)
    if recv_size != size:
        try:
            # try to unpack only opr type instead of whole header
            opr = struct.unpack('!i', buf[0:recv_size])[0]
            return (opr, 0, 0, 0)
        except:
            # raise error if unpack failed
            raise ex.SYS_COPY_LEN_ERR

    u = struct.unpack(fmt, buf)
    return u

class Encryption:
    def __init__(self, connection):
        self.algorithm = connection.account.encryption_algorithm.lower().replace('-', '_')
        self.key = connection.shared_secret
        self.key_size = connection.account.encryption_key_size

        self.ifmt = 'i'
        self.isize = struct.calcsize(self.ifmt)
        self.ibuf = bytearray(self.isize)

    def recv_int(self, sock):
        recv_size = sock.recv_into(self.ibuf, self.isize)

        if recv_size != self.isize:
            raise ex.SYS_COPY_LEN_ERR

        u = struct.unpack(self.ifmt, self.ibuf)
        return u[0]

    def send_int(self, sock, i):
        struct.pack_into(self.ifmt, self.ibuf, 0, i)

        sock.sendall(self.ibuf)

    def generate_key(self):
        return os.urandom(self.key_size)

    def __xxcrypt(self, iv, buf, op):
        cipher = M2Crypto.EVP.Cipher(alg=self.algorithm, key=self.key,
                                     iv=iv, op=op)
        return cipher.update(buf) + cipher.final()

    def decrypt(self, buf):
        iv = buf[0:self.key_size]
        text = buf[self.key_size:]
        try:
            return self.__xxcrypt(iv, text, op=0)
        except TypeError:
            # Python 2 doesn't seem to know that memoryview on bytearray
            # are bytelike objects...
            return self.__xxcrypt(bytearray(iv), bytearray(text), op=0)

    def encrypt(self, iv, buf):
        return iv + self.__xxcrypt(iv, buf, op=1)


class MultithreadDataObjectManager(DataObjectManager):

    # lib/api/include/dataObjInpOut.h
    DONE_OPR = 9999

    def download_parallel(self, irods_path, local_path, executor=None,
                          progress_cb=None, **options):

        progress_cb = progress_cb or (lambda l, i, c: True)

        def opr_complete(conn, desc):
            message = iRODSMessage('RODS_API_REQ',
                                   OprComplete(myInt=desc),
                                   int_info=api_number['OPR_COMPLETE_AN'])

            conn.send(message)
            return conn.recv()

        def recv_task(sock, local_path, conn, task_count):
            try:
                with open(local_path, 'r+b') as lf:
                    buf = memoryview(bytearray(self.READ_BUFFER_SIZE))
                    if use_encryption:
                        crypt = Encryption(conn)

                    while True:
                        opr, _, offset, size = recv_xfer_header(sock)
                        if opr == self.DONE_OPR:
                            break

                        lf.seek(offset)

                        while size > 0:
                            if task_count.value < 0:
                                return

                            to_read = min(size, self.READ_BUFFER_SIZE)

                            if use_encryption:
                                to_read = crypt.recv_int(sock)

                            all_read = 0
                            while all_read < to_read:
                                current = buf[all_read:]
                                read_size = sock.recv_into(current,
                                                           to_read - all_read)
                                all_read += read_size

                            plaintext = buf[0:all_read]

                            if use_encryption:
                                plaintext = crypt.decrypt(plaintext)
                                all_read = len(plaintext)

                            lf.write(plaintext)
                            size -= all_read

                            if not progress_cb(local_path, irods_path,
                                               all_read):
                                task_count.value = -1
                                conn.release()
            finally:
                sock.close()

            if task_count.decr() == 0:
                # last task has to complete iRODS operation
                opr_complete(conn, desc)
                conn.release()

        def write_from_response(irods_path, local_path, response, conn,
                                progress_cb):
            try:
                with open(local_path, 'wb') as lf:
                    lf.write(response.bs)

                opr_complete(conn, desc)
            finally:
                conn.release()
                progress_cb(local_path, irods_path, len(response.bs))

            return []

        # Check for force flag if local file exists
        if os.path.exists(local_path) and kw.FORCE_FLAG_KW not in options:
            raise ex.OVERWRITE_WITHOUT_FORCE_FLAG

        response, message, conn = self._open_request(irods_path,
                                                     'DATA_OBJ_GET_AN',
                                                     'r', 0, **options)

        use_encryption = hasattr(conn, 'shared_secret') and conn.shared_secret is not None

        desc = message.l1descInx

        if desc <= 2:
            # file contents are directly embeded in catalog response

            if executor is not None:
                return [executor.submit(write_from_response, irods_path,
                                        local_path, response, conn,
                                        progress_cb)]

            write_from_response(irods_path, local_path, response, conn,
                                progress_cb)
            return []

        futs = []

        nt = message.numThreads
        if nt <= 0:
            nt = 1

        host = message.PortList_PI.hostAddr
        port = message.PortList_PI.portNum
        cookie = message.PortList_PI.cookie

        task_count = LockCounter(nt)

        join = False
        if executor is None:
            # handle parallel transfer with own executor
            executor = ThreadPoolExecutor(max_workers=nt)
            join = True

        with open(local_path, 'w'):
            # create local file
            pass

        for _ in range(nt):
            sock = connect_to_portal(host, port, cookie)
            fut = executor.submit(recv_task, sock, local_path, conn,
                                  task_count)

            futs.append(fut)

        if join:
            executor.shutdown()
            exceptions = []
            for f in futs:
                e=f.exception()
                if e is not None:
                    exceptions.append(e)
            if len(exceptions) > 0:
                msgs = ['%s%s' % (type(e).__name__, str(e)) for e in exceptions]
                raise Exception(', '.join(msgs))

        return futs

    def _put_opened_file(self, local_path, obj):
        with open(local_path, 'rb') as f:
            for chunk in chunks(f, self.WRITE_BUFFER_SIZE):
                obj.write(chunk)

    def put_parallel(self, local_path, irods_path, executor=None,
                     progress_cb=None, **options):

        progress_cb = progress_cb or (lambda l, i, c: True)

        def send_task(sock, local_path, conn, task_count):
            try:
                with open(local_path, 'rb') as lf:
                    if use_encryption:
                        crypt = Encryption(conn)

                    while True:
                        opr, _, offset, size = recv_xfer_header(sock)

                        if opr == self.DONE_OPR:
                            break

                        lf.seek(offset)

                        if use_encryption:
                            iv = crypt.generate_key()

                        while size > 0:
                            if task_count.value < 0:
                                return
                            to_read = min(size, self.WRITE_BUFFER_SIZE)

                            buf = lf.read(to_read)
                            read_size = len(buf)

                            new_size = read_size
                            if use_encryption:
                                buf = crypt.encrypt(iv, buf)
                                new_size = len(buf)
                                crypt.send_int(sock, new_size)

                            sock.sendall(buf)

                            size -= read_size

                            if not progress_cb(local_path, irods_path,
                                               read_size):
                                task_count.value = -1
            finally:
                sock.close()

            if task_count.decr() == 0:
                # last task has to complete iRODS operation
                message = iRODSMessage('RODS_API_REQ',
                                       OprComplete(myInt=desc),
                                       int_info=api_number['OPR_COMPLETE_AN'])

                conn.send(message)
                conn.recv()
                conn.release()

                replicate()

        def send_task_cb(fut):
            if fut.exception() is not None:
                # exception occurred in send_task. Mark other tasks for exit
                task_count.value = -1

        def send_to_catalog(conn, local_path, irods_path, desc, **options):
            with io.BufferedRandom(iRODSDataObjectFileRaw(conn,
                                   desc, **options)) as o:
                self._put_opened_file(local_path, o)
            replicate()

        def replicate():
            if kw.ALL_KW in options:
                options[kw.UPDATE_REPL_KW] = ''
                self.replicate(irods_path, **options)

        local_size = os.lstat(local_path).st_size

        # Set operation type to trigger acPostProcForPut
        if kw.OPR_TYPE_KW not in options:
            options[kw.OPR_TYPE_KW] = 1 # PUT_OPR

        _, message, conn = self._open_request(irods_path,
                                              'DATA_OBJ_PUT_AN', 'w',
                                              local_size, **options)

        use_encryption = conn.shared_secret is not None

        desc = message.l1descInx
        nt = message.numThreads
        if nt <= 0:
            nt = 1

        futs = []
        join = False

        if executor is None:
            if nt <= 1:
                # sequential put
                send_to_catalog(conn, local_path, irods_path, desc,
                                **options)
                return []

            # handle parallel transfer with own executor
            executor = ThreadPoolExecutor(max_workers=nt)
            join = True

        if nt <= 1:
            fut = executor.submit(send_to_catalog, conn, local_path,
                                  irods_path, desc, **options)
            futs.append(fut)
        else:
            host = message.PortList_PI.hostAddr
            port = message.PortList_PI.portNum
            cookie = message.PortList_PI.cookie

            task_count = LockCounter(nt)

            for _ in range(nt):
                sock = connect_to_portal(host, port, cookie)
                fut = executor.submit(send_task, sock, local_path, conn,
                                      task_count)
                fut.add_done_callback(send_task_cb)

                futs.append(fut)

        if join:
            executor.shutdown()
            exceptions = []
            for f in futs:
                e=f.exception()
                if e is not None:
                    exceptions.append(e)
            if len(exceptions) > 0:
                msgs = ['%s%s' % (type(e).__name__, str(e)) for e in exceptions]
                raise Exception(', '.join(msgs))

        return futs

    def _open_request(self, path, an_name, mode, size, **options):
        if kw.DEST_RESC_NAME_KW not in options:
            # Use client-side default resource if available
            try:
                options[kw.DEST_RESC_NAME_KW] = self.sess.default_resource
            except AttributeError:
                pass

        try:
            oprType = options[kw.OPR_TYPE_KW]
        except KeyError:
            oprType = 0

        flags, seek_to_end = {
            'r': (self.O_RDONLY, False),
            'r+': (self.O_RDWR, False),
            'w': (self.O_WRONLY | self.O_CREAT | self.O_TRUNC, False),
            'w+': (self.O_RDWR | self.O_CREAT | self.O_TRUNC, False),
            'a': (self.O_WRONLY | self.O_CREAT, True),
            'a+': (self.O_RDWR | self.O_CREAT, True),
        }[mode]
        # TODO: Use seek_to_end

        message_body = FileOpenRequest(
            objPath=path,
            createMode=0,
            openFlags=flags,
            offset=0,
            dataSize=size,
            numThreads=self.sess.numThreads,
            oprType=oprType,
            KeyValPair_PI=StringStringMap(options),
        )

        message = iRODSMessage('RODS_API_REQ', msg=message_body,
                               int_info=api_number[an_name])

        conn = self.sess.pool.get_connection()
        conn.send(message)
        resp = conn.recv()

        return resp, resp.get_main_message(PortalOprResponse), conn

