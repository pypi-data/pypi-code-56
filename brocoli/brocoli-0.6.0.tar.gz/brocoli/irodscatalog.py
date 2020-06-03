"""
Implements iRODS Catalog object and methods
"""

from . import catalog
from . import form
from . import exceptions
from . listmanager import ColumnDef, List
from . config_option import option_is_true

from . irodsdom import ModifiedDataObjectManager

import re
import os
import io
import hashlib
import base64
import collections
import datetime
import ssl
import time

from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
from queue import Queue
from threading import Lock

from six import print_
from six.moves import tkinter as tk

import irods
from irods.session import iRODSSession
from irods import password_obfuscation
from irods.manager.data_object_manager import DataObjectManager
from . irodsdom import MultithreadDataObjectManager
from irods.manager.collection_manager import CollectionManager
from irods.models import DataObject, Collection
from irods.manager import data_object_manager
from irods.data_object import chunks
from irods.column import Like
from irods.api_number import api_number
import irods.keywords as kw
import irods.constants as const
import irods.message as message
import irods.exception

_getuid = None
if hasattr(os, 'getuid'):
    _getuid = os.getuid
else:
    import getpass

    # generate a fake uid on systems that lacks os.getuid()
    def _fake_getuid():
        return int('0x' + hashlib.md5(getpass.getuser().encode()).hexdigest(),
                   16) % 10000

    _getuid = _fake_getuid


def parse_env3(path):
    """
    parse iRODS v3 iCommands environment files
    """

    pat = ("^\s*(?P<name>\w+)" + "(\s+|\s*=\s*)[\'\"]?(?P<value1>[^\'\"\n]*)" +
           "[\'\"]?\s*$")
    envre = re.compile(pat)

    ret = {}

    with open(path, 'r') as f:
        for l in f.readlines():
            m = envre.match(l)
            if m:
                ret[m.group("name")] = m.group("value1")

    return ret


def local_trees_stats(dirs):
    """
    Gathers stats (number of files and cumulated size) of sub-trees on a local
    directories list
    """
    total_nfiles = 0
    total_size = 0
    stats = {}

    for d in dirs:
        nfiles = 0
        size = 0

        for root, dirs, files in os.walk(d):
            nfiles += len(files)
            size += sum(os.path.getsize(os.path.join(root, name))
                        for name in files)
        stats[d] = size

        total_nfiles += nfiles
        total_size += size

    return total_nfiles, total_size, stats


def local_files_stats(files):
    """
    Computes stats (number of files and cumulated size) on a file list
    """
    stats = {f: os.path.getsize(f) for f in files}
    return len(files), sum(v for v in stats.values()), stats


def method_translate_exceptions(method):
    """
    Method decorator that translates iRODS to Brocoli exceptions
    """
    def method_wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except irods.exception.CAT_INVALID_AUTHENTICATION as e:
            self.close()
            raise exceptions.ConnectionError(e)
        except (irods.exception.NetworkException, ssl.SSLError) as e:
            raise exceptions.NetworkError(e)
        except irods.exception.CAT_UNKNOWN_COLLECTION as e:
            raise exceptions.FileNotFoundError(e)
        except irods.exception.CAT_SQL_ERR as e:
            raise exceptions.CatalogLogicError(e)
        except irods.exception.SYS_FILE_DESC_OUT_OF_RANGE as e:
            raise exceptions.CatalogLogicError(e)

    return method_wrapper


def function_translate_exceptions(func):
    """
    Function decorator that translates iRODS to Brocoli exceptions
    """
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except irods.exception.CAT_INVALID_AUTHENTICATION as e:
            raise exceptions.ConnectionError(e)
        except irods.exception.NetworkException as e:
            raise exceptions.NetworkError(e)
        except irods.exception.CAT_UNKNOWN_COLLECTION as e:
            raise exceptions.FileNotFoundError(e)
        except irods.exception.CAT_SQL_ERR as e:
            raise exceptions.CatalogLogicError(e)
        except irods.exception.SYS_FILE_DESC_OUT_OF_RANGE as e:
            raise exceptions.CatalogLogicError(e)

    return function_wrapper


def splitsize(size, n, bs):
    # generate a sequence of offsets and chunk size based on n (nb of threads)
    # and bs (block size)

    # number of blocks
    nb = max(0, (size - 1) // bs) + 1

    # ensure each thread has at least 2 chunks
    n = max(1, min(n, nb//2))

    d, m = divmod(nb, n)

    p = 0
    for i in range(m):
        yield p*bs, (d + 1)*bs
        p += d + 1

    for i in range(m, n):
        yield p*bs, min(d*bs, size - p*bs)
        p += d


class LockedSession:
    class LockedDOM:
        def __init__(self, dom, lock=None):
            self.dom = dom
            self.lock = lock or Lock()

        def open(self, *args, **kwargs):
            with self.lock:
                return self.dom.open(*args, **kwargs)

        def replicate(self, *args, **kwargs):
            with self.lock:
                return self.dom.replicate(*args, **kwargs)

        def truncate(self, *args, **kwargs):
            with self.lock:
                return self.dom.truncate(*args, **kwargs)

        def unlink(self, *args, **kwargs):
            with self.lock:
                return self.dom.unlink(*args, **kwargs)

        def get(self, *args, **kwargs):
            with self.lock:
                return self.dom.get(*args, **kwargs)

    def __init__(self, session, lock=None):
        self.session = session
        self.lock = lock or Lock()

    @property
    def data_objects(self):
        return self.LockedDOM(MultithreadDataObjectManager(self.session), self.lock)

    def query(self, *args, **kwargs):
        #with self.lock:
        return self.session.query(*args, **kwargs)


class ExecutorPair:
    # consists in:
    # * a pair of ThreadPoolExecutor. One for transfers, the
    #   second for compute tasks.
    # * a queue to yield advancement to progressbar

    def __init__(self, session, xnt, cnt):
        self.session = LockedSession(session)
        self.xnt = xnt
        self.cnt = cnt
        self.xpe = ThreadPoolExecutor(max_workers=xnt)
        self.cpe = ThreadPoolExecutor(max_workers=cnt)

        self.interrupted = False

        # list of pending tasks
        self.xfer_futures = []
        self.compute_futures = []

        # locks for manipulating futures lists
        self.xfer_lock = Lock()
        self.compute_lock = Lock()

        # queue used to yield advancement to progressbar
        self.yield_queue = Queue()

    # context manager behaviour
    def __enter__(self):
            return self

    def __exit__(self, type, value, traceback):
        # cancel all pending xfer tasks
        for f in self.xfer_futures:
            f.cancel()

        # mark running tasks for immediate interruption
        self.interrupted = True

        # shutdown executors
        self.xpe.shutdown(wait=True)
        self.cpe.shutdown(wait=True)

    def submit_xfer(self, func, args, completed_cb=None):
        fut = self.xpe.submit(func, *args)
        return self.add_xfer_future(fut, completed_cb)

    def add_xfer_future(self, fut, completed_cb=None):
        if completed_cb is not None:
            fut.add_done_callback(completed_cb)

        with self.xfer_lock:
            self.xfer_futures.append(fut)

        return fut

    def submit_compute(self, func, args, completed_cb=None):
        fut = self.cpe.submit(func, *args)
        if completed_cb is not None:
            fut.add_done_callback(completed_cb)

        with self.compute_lock:
            self.compute_futures.append(fut)

        return fut

    def wait_xfer(self, timeout):
        with self.xfer_lock:
            completed, futures = wait(self.xfer_futures, timeout, FIRST_COMPLETED)
            self.xfer_futures = list(futures)

    def wait_compute(self, timeout):
        with self.compute_lock:
            completed, futures = wait(self.compute_futures, timeout, FIRST_COMPLETED)
            self.compute_futures = list(futures)

    def wait(self, xfer_timeout, compute_timeout):
        self.wait_xfer(xfer_timeout)
        self.wait_compute(compute_timeout)

    def pending_tasks(self):
        with self.xfer_lock, self.compute_lock:
            return len(self.xfer_futures) + len(self.compute_futures)

    def yq_put(self, element):
        self.yield_queue.put(element)

    def progress(self, osl):
        progress = 0
        while not self.yield_queue.empty():
            path, y = self.yield_queue.get()
            os = osl[path]

            if y is None:
                # file operation is finished, mark operation as done
                if os.status == catalog.OperationStatus.IN_PROGRESS:
                    os.done()
                continue

            os.progress += y
            progress += y

        return progress

    def wait_progress(self, timeout, osl):
        timeout *= 0.5

        while self.pending_tasks() > 0:
            self.wait(timeout, timeout)
            p = self.progress(osl)
            if p > 0:
                yield p

class LockedCounter:
    def __init__(self, value=0):
        self.lock = Lock()
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def set(self, new_value):
        with self.lock:
            self.__value = new_value
            return self.__value

    def __add(self, add):
        with self.lock:
            self.__value += add
            return self.__value

    def incr(self, increment=1):
        return self.__add(increment)

    def decr(self, decrement=1):
        return self.__add(- decrement)

class iRODSCatalogBase(catalog.Catalog):
    """
    A base class Catalog for connecting to iRODS
    """

    BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE * 1024

    def local_file_cksum(self, filename, algorithm=None):
        def get_digest(h):
            if h.name == 'sha256':
                return 'sha2:' + base64.b64encode(h.digest()).decode()

            return h.hexdigest()

        if algorithm is None:
            algorithm = 'md5'
            if self.session.pool.account.default_hash_scheme == 'SHA256':
                algorithm = 'sha256'

        scheme = hashlib.new(algorithm)
        with open(filename, 'rb') as f:
            for chunk in chunks(f, self.BUFFER_SIZE):
                scheme.update(chunk)
                yield len(chunk), ''

        yield 0, get_digest(scheme)

    def local_file_cksum_ref(self, filename, ref_cksum):
        algorithm = None
        if ref_cksum is None:
            algorithm = 'sha256' if self.session.pool.account.default_hash_scheme == 'SHA256' else 'md5'
        elif ref_cksum.startswith('sha2:'):
            algorithm = 'sha256'

        for y in self.local_file_cksum(filename, algorithm):
            yield y

    @classmethod
    def encode(cls, s):
        return password_obfuscation.encode(s, _getuid())

    @classmethod
    def decode(cls, s):
        return password_obfuscation.decode(s, _getuid())

    def __init__(self, session, default_resc, local_checksum,
                 xfer_nt=1):
        self.session = session

        self.default_resc = default_resc

        self.local_checksum = local_checksum

        self.dom = MultithreadDataObjectManager(self.session)
        self.cm = self.session.collections
        self.am = self.session.permissions
        self.xfer_nt = xfer_nt

    def close(self):
        self.session.cleanup()

    def cksum_factor(self):
        return 2 if self.local_checksum else 1

    def splitname(self, path):
        return path.rsplit('/', 1)

    def basename(self, path):
        _, basename = self.splitname(path)
        return basename

    def dirname(self, path):
        dirname, _ = self.splitname(path)
        return dirname

    def normpath(self, path):
        pathlist = []

        for t in path.split('/'):
            if t == '' or t == '.':
                continue

            if t == '..':
                if len(pathlist):
                    del pathlist[-1]
                continue

            pathlist.append(t)

        normpath = '/'.join([''] + pathlist)

        return normpath or '/'

    @method_translate_exceptions
    def lstat(self, path):
        if self.isdir(path):
            return self.lstat_dir(path)
        return self.lstat_file(path)

    def lstat_dir(self, path):
        q = self.session.query(Collection.owner_name)
        q = q.filter(Collection.name == path)

        r = q.one()

        ret = {
            'user': r[Collection.owner_name],
            'size': '',
            'mtime': '',
            'nreplicas': '',
            'isdir': True,
        }

        return ret

    def lstat_dirs(self, parent_path):
        q = self.session.query(Collection.name, Collection.owner_name)
        q = q.filter(Collection.parent_name == parent_path)

        ret = {}
        for r in q.get_results():

            ret[self.basename(r[Collection.name])] = {
                'user': r[Collection.owner_name],
                'size': '',
                'mtime': '',
                'nreplicas': '',
                'isdir': True,
            }

        return ret

    def lstat_files(self, dirname):
        epoch = datetime.datetime(1, 1, 1)

        q = self.session.query(DataObject.name, DataObject.owner_name,
                               DataObject.size,
                               DataObject.modify_time,
                               DataObject.replica_number)
        q = q.filter(Collection.name == dirname)

        ret = {}
        for r in q.get_results():
            name = r[DataObject.name]
            dobj = ret.get(name, {'minsize': None, 'maxsize': 0,
                                  'mtime': epoch, 'isdir': False,
                                  'nreplicas': 0})

            dobj['user'] = r[DataObject.owner_name]
            dobj['nreplicas'] += 1

            mtime = r[DataObject.modify_time]
            if mtime > dobj['mtime']:
                dobj['mtime'] = mtime

            size = r[DataObject.size]
            if dobj['minsize'] is None or size < dobj['minsize']:
                dobj['minsize'] = size

            if size > dobj['maxsize']:
                dobj['maxsize'] = size

            ret[name] = dobj

        for k, v in ret.items():
            minsize = v['minsize']
            maxsize = v['maxsize']
            if maxsize != minsize:
                v['size'] = '{}-{}'.format(minsize, maxsize)
            else:
                v['size'] = str(minsize)

        return ret

    def lstat_file(self, path):
        dirname, basename = self.splitname(path)
        q = self.session.query(DataObject.owner_name, DataObject.size,
                               DataObject.modify_time,
                               DataObject.replica_number)
        q = q.filter(Collection.name == dirname)
        q = q.filter(DataObject.name == basename)

        replicas = q.all()
        if len(replicas) < 1:
            # no replica
            raise exceptions.ioerror(exceptions.errno.ENOENT)

        ret = {'nreplicas': len(replicas), 'isdir': False}
        minsize = None
        maxsize = 0
        for r in replicas:
            ret['user'] = r[DataObject.owner_name]
            ret['mtime'] = r[DataObject.modify_time]
            size = r[DataObject.size]
            if minsize is None or size < minsize:
                minsize = size
            if size > maxsize:
                maxsize = size

        if maxsize != minsize:
            ret['size'] = '{}-{}'.format(minsize, maxsize)
        else:
            ret['size'] = str(minsize)

        return ret

    @method_translate_exceptions
    def listdir(self, path):
        q = self.session.query(DataObject.name).filter(Collection.name == path)
        files = [r[DataObject.name] for r in q.all()]

        q = self.session.query(Collection.name) \
            .filter(Collection.parent_name == path)
        colls = [self.basename(c[Collection.name]) for c in q.all()]

        ret = self.lstat_dirs(path)
        ret.update(self.lstat_files(path))

        return ret

    @method_translate_exceptions
    def isdir(self, path):
        q = self.session.query(Collection.id).filter(Collection.name == path)

        try:
            q.one()
        except irods.exception.NoResultFound:
            return False

        return True

    def join(self, *args):
        return '/'.join(args)

    def remote_files_stats(self, file_paths):
        dirs = {self.dirname(p) for p in file_paths}

        stats = {}
        for d in dirs:
            q = self.session.query(DataObject.name, DataObject.size)
            q = q.filter(Collection.name == d)

            for r in q.get_results():
                stats[self.join(d, r[DataObject.name])] = \
                  int(r[DataObject.size])

        return (len(file_paths),
                sum([v for k, v in stats.items() if k in file_paths]),
                stats)

    def remote_trees_stats(self, dirs):
        nfiles = 0
        size = 0
        stats = {}

        for d in dirs:
            # need to keep column 'collection_id' to avoid 'distinct' clause on
            # recursive queries
            q = self.session.query(DataObject.collection_id, DataObject.name,
                                   DataObject.size)

            dsize = 0
            # first level query
            q1 = q.filter(Collection.name == d)
            for r in q1.get_results():
                nfiles += 1
                dsize += int(r[DataObject.size])

            # recursive query
            qr = q.filter(Like(Collection.name, self.join(d, '%')))
            for r in qr.get_results():
                nfiles += 1
                dsize += int(r[DataObject.size])

            stats[d] = dsize
            size += dsize

        return nfiles, size, stats

    def _register_data_objects_in_osl(self, pathlist, osl):
        def _cancel_cb(op_stat):
            print_('Operation', op_stat.print_status(),
                   ': delete', op_stat.current_element)
            os.unlink(op_stat.current_element)

        nfiles, file_size, fstats = self.remote_files_stats(pathlist)

        cksum_factor = self.cksum_factor()
        stats = {k : (s * cksum_factor) for k, s in fstats.items()}
        osl.update_list(pathlist, size=stats, file_size=fstats,
                        cancel=_cancel_cb)


        return nfiles, file_size, file_size * cksum_factor

    @method_translate_exceptions
    def download_files(self, pathlist, destdir, osl):
        t0 = time.time()

        nfiles, file_size, size = self._register_data_objects_in_osl(pathlist, osl)

        if nfiles > 1 or size > self.BUFFER_SIZE:
            # wake up progress bar for more than one file or one large file
            yield 0, size

        completed = 0
        with ExecutorPair(self.session, self.xfer_nt, cnt=4) as ep:
            for y in self._download_files(pathlist, destdir, osl, ep):
                completed += y
                yield completed, size

            # actively wait for all tasks to finish
            for p in ep.wait_progress(0.1, osl):
                completed += p
                yield completed, size

        elapsed = time.time() - t0
        if elapsed > 0:
            print_('download_files finished', elapsed, 'seconds (%.2f MB/s)' % (file_size / (elapsed * 10**6)))

    def _download_files(self, irods_paths, local_dir, osl, ep):
        # local functions
        # ---------------
        def _submit_read(ep, irods_path, local_path, **options):
            @function_translate_exceptions
            def _read(p, s, task_num):
                f = dom.open(irods_path, 'r', **options)
                fd = os.open(local_path, os.O_WRONLY, 0o640)

                try:
                    buf = bytearray(self.BUFFER_SIZE)
                    read = 0
                    origp = p
                    #print_('thread if={} p={} s={} fd={}'.format(irods_path, p, s, fd))
                    f.seek(p)
                    os.lseek(fd, p, os.SEEK_SET)
                    while s > 0:
                        if ep.interrupted:
                            return

                        to_read = min(self.BUFFER_SIZE, s)
                        mv = memoryview(buf)[0:to_read]
                        l = f.readinto(mv)
                        if l != to_read:
                            raise IOError('[%s->%s] error reading %s expected %s' % (irods_path, local_path, l, to_read))

                        os.write(fd, mv)
                        p += l
                        s -= l
                        read += l

                        ep.yq_put((irods_path, l))
                        #print_('%s read %s, remaining %s' % (origp, read, s))

                finally:
                    f.close()
                    os.close(fd)

                return irods_path, local_path, read

            dom = ep.session.data_objects

            fsize = osl[irods_path].file_size

            with open(local_path, 'wb+') as lf:
                lf.truncate(fsize)

            i = 0
            futures = []
            for p, s in splitsize(fsize, ep.xnt, self.BUFFER_SIZE):
                print_(time.time(), 'submit read', irods_path, p, s, fsize)
                fut = ep.submit_xfer(_read, (p, s, i), _submit_validate)
                futures.append(fut)
                i += 1

            return futures

        def progress_cb(local_path, irods_path, count):
            print_('progress', local_path, irods_path, count)
            ep.yq_put((irods_path, count))

        def _submit_validate(fut):
            # validate downloaded file (from xfer future fut)

            @function_translate_exceptions
            def _validate(irods_path, local_path):
                print_(time.time(), 'validating file', local_path)
                obj = self.dom.get(irods_path)

                completed = 0

                for l, local_cksum in self.local_file_cksum_ref(local_path, obj.checksum):
                    if ep.interrupted:
                        return

                    completed += l

                    ep.yq_put((irods_path, l))

                if obj.checksum is None:
                    print_('WARNING: iRODS checksum is None', irods_path, local_cksum)
                elif obj.checksum != local_cksum:
                    msg = 'Downloaded file {} has an incorrect checksum ' \
                           '(local=\'{}\', ' \
                           'catalog=\'{}\')'.format(irods_path, local_cksum, obj.checksum)
                    osl[irods_path].fail(exceptions.ChecksumError(msg))
                else:
                    print_('checksum ok', irods_path, local_cksum)

                # tell file validation is finished
                ep.yq_put((irods_path, None))

            if fut.cancelled() or ep.interrupted:
                # bailout since result is not available
                return

            op_stat = fut2os[fut]
            del fut2os[fut]

            e = fut.exception()
            if e is not None:
                print_('ERROR: caught some exception', e)
                op_stat.fail(e)
                return

            #ip, lp, read_bytes = fut.result()
            ip, lp = fut2files[fut]
            files[(ip, lp)] -= 1

            # whole file downloaded: submit validation task
            if files[(ip, lp)] == 0:
                if not self.local_checksum:
                    # checksum not needed: tell file validation is finished
                    ep.yq_put((ip, None))
                    return

                vfut = ep.submit_compute(_validate, (ip, lp), fut_handle_exception)
                fut2os[vfut] = op_stat

        def fut_handle_exception(fut):
            e = fut.exception()
            if e is not None:
                print_('ERROR: got some exception', e)
                fut2os[fut].fail(e)

        # method code
        # -----------

        options = {
            kw.FORCE_FLAG_KW: True,
        }

        files = {}
        fut2os = {}
        fut2files = {}

        # submit transfer tasks
        for irods_path in irods_paths:
            _, fn = irods_path.rsplit('/', 1)
            local_path = os.path.join(local_dir, fn)

            osl[irods_path].in_progress(local_path)
            print_('in progress', irods_path)
#            futs = _submit_read(ep, irods_path, local_path, **options)
            futs = self.dom.download_parallel(irods_path, local_path, ep.xpe,
                                              progress_cb=progress_cb, **options)
            for fut in futs:
                ep.add_xfer_future(fut, completed_cb=_submit_validate)
                fut2files[fut] = irods_path, local_path

            files[(irods_path, local_path)] = len(futs)
            fut2os.update({fut : osl[irods_path] for fut in futs})

            # check already finished transfer tasks
            ep.wait_xfer(0)
            ep.wait_compute(0)
            p = ep.progress(osl)
            if p > 0:
                yield p
                
        yield ep.progress(osl)

    def _download_coll(self, coll, destdir, osl, ep):
        destdir = os.path.join(destdir, coll.name)
        try:
            os.makedirs(destdir)
        except OSError:
            if not os.path.isdir(destdir):
                raise

        print_('begin coll', coll.name, 'subcolls', list(coll.subcollections))

        pathlist = [dobj.path for dobj in list(coll.data_objects)]
        osl.add_keys(pathlist)
        self._register_data_objects_in_osl(pathlist, osl)
        for y in self._download_files(pathlist, destdir, osl, ep):
            yield y

        for subcoll in coll.subcollections:
            for y in self._download_coll(subcoll, destdir, osl, ep):
                yield y

    @method_translate_exceptions
    def download_directories(self, pathlist, destdir, osl):
        t0 = time.time()

        nfiles, file_size, fstats = self.remote_trees_stats(pathlist)
        cksum_factor = self.cksum_factor()
        size = file_size * cksum_factor

        with ExecutorPair(self.session, self.xfer_nt, cnt=4) as ep:
            completed = 0
            for p in pathlist:
                coll = self.cm.get(p)
                for y in self._download_coll(coll, destdir, osl, ep):
                    completed += y
                    yield completed, size

            # actively wait for all tasks to finish
            for p in ep.wait_progress(0.1, osl):
                completed += p
                yield completed, size

        elapsed = time.time() - t0
        if elapsed > 0:
            print_('download_directories finished', elapsed, 'seconds (%.2f MB/s)' % (file_size / (elapsed * 10**6)))

    @method_translate_exceptions
    def upload_files(self, files, path, osl):
        t0 = time.time()

        nfiles, fsize, fstats = local_files_stats(files)

        def cancel(op_stat):
            print_('Operation', op_stat.print_status(),
                   ': delete', op_stat.current_element)
            try:
                self.dom.unlink(op_stat.current_element, force=True)
            except irods.exception.CAT_NO_ROWS_FOUND:
                # don't care if file is not found: catalog may have
                # removed it already
                pass

        cksum_factor = self.cksum_factor()
        size = fsize * cksum_factor
        stats = {k : (s * cksum_factor) for k, s in fstats.items()}
        osl.update_list(files, size=stats, file_size=fstats, cancel=cancel)

        with ExecutorPair(self.session, self.xfer_nt, cnt=4) as ep:
            completed = 0
            for s in self._upload_files(files, path, osl, ep):
                completed += s
                yield completed, size

            # actively wait for all tasks to finish
            for p in ep.wait_progress(0.1, osl):
                completed += p
                yield completed, size

        elapsed = time.time() - t0
        if elapsed > 0:
            print_('upload_files finished in', elapsed,
                   'seconds (%.2f MB/s)' % (fsize/elapsed / 10**6))

    def _upload_files(self, files, path, osl, ep):
        def _upload(local_path, irods_path, op_stat, p, s, lc, cksum,
                    options):
            with open(local_path, 'rb') as f:
                dom = ep.session.data_objects
                o = dom.open(irods_path, 'a+', **options)

                f.seek(p)
                o.seek(p)

                completed = 0
                while completed < s:
                    if ep.interrupted:
                        break
                    chunk = f.read(self.BUFFER_SIZE)
                    l = len(chunk)
                    o.write(chunk)
                    completed += l
                    ep.yq_put((local_path, l))

                o.close()


            # we are the last upload task
            if lc.decr() == 0:
                print_(time.time(), 'ok xfer finished', local_path, p, p+s, cksum)

                opts = options.copy()

                # Set operation type to trigger acPostProcForPut
                opts[kw.OPR_TYPE_KW] = 1  # PUT_OPR
                if cksum is not None:
                    opts[kw.VERIFY_CHKSUM_KW] = cksum

                if ep.interrupted:
                    return

                o = dom.open(irods_path, 'a+', **opts)
                o.close()

                if kw.ALL_KW in opts:
                    opts[kw.UPDATE_REPL_KW] = ''

                    if ep.interrupted:
                        return

                    dom.replicate(irods_path, **opts)

                if ep.interrupted:
                    return

                ep.yq_put((local_path, None))

        def submit_compute_checksum(lf, op_stat):
            # variables lf and op_stat are used in local functions
            def _compute_checksum():
                def _upload_completed_cb(fut):
                    if fut.cancelled():
                        return

                    e = fut.exception()
                    if e is not None:
                        print_(lf, '_upload failed with exception', e)
                        op_stat.fail(e)
                        return

                print_(time.time(), 'begin _compute_checksum', lf)

                cksum = None
                if self.local_checksum:
                    l = 0
                    for l, cksum in self.local_file_cksum(lf):
                        ep.yq_put((lf, l))

                try:
                    # overwrite an existing file in parallel seems to be
                    # a bad idea, so delete it if necessary
                    ep.session.data_objects.unlink(op_stat.current_element)
                except irods.exception.CAT_NO_ROWS_FOUND:
                    pass

                file_parts = list(splitsize(op_stat.file_size, ep.xnt,
                                  self.BUFFER_SIZE))

                xfer_counter = LockedCounter(len(file_parts))

                if ep.interrupted:
                    return

                for p, s in file_parts:
                    print_(time.time(), 'submit _upload', lf, p, p + s, op_stat.file_size)
                    ep.submit_xfer(_upload, (lf, op_stat.current_element,
                                             op_stat, p, s, xfer_counter,
                                             cksum, options),
                                   _upload_completed_cb)

            def _completed_cb(fut):
                if fut.cancelled():
                    return

                e = fut.exception()
                if e is not None:
                    print_(lf, 'compute checksum failed with exception', e)
                    op_stat.fail(e)
                    return

            print_(time.time(), 'submit _compute_checksum', lf)
            fut = ep.submit_compute(_compute_checksum, [], _completed_cb)

        # method code
        #############
        if not path.endswith('/'):
            path = path + '/'

        options = {
            kw.ALL_KW: '',
            kw.UPDATE_REPL_KW: '',
        }

        if self.default_resc is not None:
            options[kw.DEST_RESC_NAME_KW] = self.default_resc

        for f in files:
            basename = os.path.basename(f)
            irods_path = path + basename

            osl[f].in_progress(irods_path)

            submit_compute_checksum(f, osl[f])

            ep.wait(0, 0)
            y = ep.progress(osl)
            yield y

    def _upload_dir(self, dir_, path, osl, ep):
        print_(time.time(), '_upload_dir begin', dir_)
        files = []
        subdirs = []

        try:
            self.cm.create(path)
        except irods.exception.CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME:
            pass

        for name in os.listdir(dir_):
            abspath = os.path.join(dir_, name)
            if os.path.isdir(abspath):
                subdirs.append((abspath, name))
            else:
                files.append(abspath)

        nfiles, fsize, fstats = local_files_stats(files)

        def cancel(op_stat):
            print_('Operation', op_stat.print_status(),
                   ': delete', op_stat.current_element)
            try:
                self.dom.unlink(op_stat.current_element, force=True)
            except irods.exception.CAT_NO_ROWS_FOUND:
                # don't care if file is not found: catalog may have
                # removed it already
                pass

        cksum_factor = self.cksum_factor()
        stats = {k : (s * cksum_factor) for k, s in fstats.items()}
        osl.add_keys(files)
        osl.update_list(files, size=stats, file_size=fstats, cancel=cancel)

        for abspath, name in subdirs:
            cpath = self.join(path, name)

            for y in self._upload_dir(abspath, cpath, osl, ep):
                yield y

        for y in self._upload_files(files, path, osl, ep):
            yield y

        print_(time.time(), '_upload_dir end', dir_)

    @method_translate_exceptions
    def upload_directories(self, dirs, path, osl):
        t0 = time.time()
        print_(t0, 'upload_directories', dirs)
        nfiles, fsize, stats = local_trees_stats(dirs)

        cksum_factor = self.cksum_factor()
        size = fsize * cksum_factor

        with ExecutorPair(self.session, self.xfer_nt, cnt=4) as ep:
            completed = 0
            for d in dirs:
                name = os.path.basename(d)
                cpath = self.join(path, name)

                for s in self._upload_dir(d, cpath, osl, ep):
                    completed += s
                    yield completed, size

            # actively wait for all tasks to finish
            for p in ep.wait_progress(0.1, osl):
                completed += p
                yield completed, size

        elapsed = time.time() - t0
        if elapsed > 0:
            print_('upload_directories finished in', elapsed,
                   'seconds (%.2f MB/s)' % (fsize/elapsed / 10**6))

    @method_translate_exceptions
    def delete_files(self, files, osl):
        number = len(files)

        i = 0
        for f in files:
            osl[f].size=1
            osl[f].in_progress(None)
            self.dom.unlink(f, force=True)
            osl[f].done()
            i += 1
            yield i, number

    def _coll_remove_yield(self, path, recurse=True, force=False, **options):
        """
        interruptible version of CollectionManager.coll_remove() method
        """
        if recurse:
            options[kw.RECURSIVE_OPR__KW] = ''
        if force:
            options[kw.FORCE_FLAG_KW] = ''

        try:
            oprType = options[kw.OPR_TYPE_KW]
        except KeyError:
            oprType = 0

        message_body = message.CollectionRequest(
            collName=path,
            flags = 0,
            oprType = oprType,
            KeyValPair_PI=message.StringStringMap(options)
        )
        msg = message.iRODSMessage('RODS_API_REQ', msg=message_body,
                                   int_info=api_number['RM_COLL_AN'])
        with self.session.pool.get_connection() as conn:
            conn.send(msg)
            response = conn.recv()

            try:
                while response.int_info == const.SYS_SVR_TO_CLI_COLL_STAT:
                    conn.reply(const.SYS_CLI_TO_SVR_COLL_STAT_REPLY)
                    yield
                    response = conn.recv()
            except GeneratorExit:
                # destroy connection which is in a bad state (could fix?)
                conn.release(destroy=True)

    @method_translate_exceptions
    def delete_directories(self, directories, osl):
        number = len(directories)

        i = 0
        for d in directories:
            osl[d].size=1
            osl[d].in_progress(None)
            for y in self._coll_remove_yield(d, recurse=True, force=True):
                yield i, number
            osl[d].done()
            i += 1
            yield i, number

    @method_translate_exceptions
    def mkdir(self, path):
        self.cm.create(path)

    def __acls_from_object(self, obj):
        access = self.am.get(obj)

        acls = [a.__dict__.copy() for a in access]

        for a in acls:
            # build a unique ttk.TreeWidget iid
            a['iid'] = '#'.join([a[t] for t in ['user_name', 'user_zone',
                                                'access_name']])
            a['#0'] = a['user_name']

        @function_translate_exceptions
        def add(result):
            access_name = result['access_name']
            user_name = result['#0']
            user_zone = result['user_zone']

            acl = irods.access.iRODSAccess(access_name, obj.path, user_name,
                                           user_zone)

            self.session.permissions.set(acl)

            return '#'.join([user_name, user_zone, access_name])

        @function_translate_exceptions
        def remove(result):
            user_name = result['#0']
            user_zone = result['user_zone']

            acl = irods.access.iRODSAccess('null', obj.path, user_name,
                                           user_zone)

            self.session.permissions.set(acl)

        acls_def = iRODSCatalogBase.acls_def(self.session.zone)

        return List(acls_def, acls, add_cb=add, remove_cb=remove)

    def __metadata_from_object(self, obj):
        metadata = [md.__dict__.copy() for md in obj.metadata.items()]

        for md in metadata:
            md['iid'] = md['avu_id']
            md['#0'] = md['name']

        @function_translate_exceptions
        def add(result):
            name = result['#0']
            value = result['value']
            units = result['units']

            obj.metadata.add(name, value, units)

            for md in obj.metadata.items():
                if md.name == name and md.value and md.units == units:
                    return md.avu_id

            return None

        @function_translate_exceptions
        def remove(result):
            name = result['#0']
            value = result['value']
            unit = result['units']

            obj.metadata.remove(name, value, unit)

        return List(iRODSCatalogBase.metadata_def(), metadata, add_cb=add,
                    remove_cb=remove)

    @method_translate_exceptions
    def directory_properties(self, path):
        co = self.cm.get(path)
        acls_list = self.__acls_from_object(co)
        metadata_list = self.__metadata_from_object(co)

        inheritance = self.session.query(Collection.inheritance) \
            .filter(Collection.name == path).one()[Collection.inheritance] \
            == '1'

        def inheritance_changed(value):
            name = 'inherit' if value else 'noinherit'
            acl = irods.access.iRODSAccess(name, path, '', '')

            self.session.permissions.set(acl)

        f = form.BooleanField('Inherit:', inheritance,
                              state_change_cb=inheritance_changed)
        inherit_frame = form.FrameGenerator([f])

        return collections.OrderedDict([
            ('Permissions', acls_list),
            ('Metadata', metadata_list),
            ('Inheritance', inherit_frame),
        ])

    @method_translate_exceptions
    def file_properties(self, path):
        do = self.dom.get(path)
        replicas = [r.__dict__.copy() for r in do.replicas]
        for r in replicas:
            # set row title for ListManager use
            r['#0'] = r['number']

        replicas_list = List(iRODSCatalogBase.replicas_def(), replicas)

        acls_list = self.__acls_from_object(do)
        metadata_list = self.__metadata_from_object(do)

        return collections.OrderedDict([
            ('Replicas', replicas_list),
            ('Permissions', acls_list),
            ('Metadata', metadata_list),
        ])

    @classmethod
    def replicas_def(cls):
        repl_num = ColumnDef('#0', 'Number',
                             form_field=form.IntegerField('Replica number:',
                                                          -1))
        resc = ColumnDef('resource_name', 'Resource',
                         form_field=form.TextField('Resource name:'))
        path = ColumnDef('path', 'Path',
                         form_field=form.TextField('Replica path:'))
        status = ColumnDef('status', 'Status',
                           form_field=form.TextField('Replica status:'))
        checksum = ColumnDef('checksum', 'Checksum',
                             form_field=form.TextField('Replica checksum:'))

        cols = [repl_num, resc, status, checksum, path]

        return collections.OrderedDict([(cd.name, cd) for cd in cols])

    @classmethod
    def acls_def(cls, default_zone=''):
        user = ColumnDef('#0', 'User', form_field=form.TextField('User:'))
        zone = ColumnDef('user_zone', 'Zone',
                         form_field=form.TextField('User zone:', default_zone))
        access_types = ['read', 'write', 'own']
        type = ColumnDef('access_name', 'Access type',
                         form_field=form.ComboboxChoiceField('Acces type:',
                                                             access_types,
                                                             access_types[0]))

        cols = [user, zone, type]

        return collections.OrderedDict([(cd.name, cd) for cd in cols])

    @classmethod
    def metadata_def(cls):
        name = ColumnDef('#0', 'Name',
                         form_field=form.TextField('Metadata name:'))
        value = ColumnDef('value', 'Value',
                          form_field=form.TextField('Metadata value:'))
        unit = ColumnDef('units', 'Unit',
                         form_field=form.TextField('Metadata unit:'))

        cols = [name, value, unit]

        return collections.OrderedDict([(cd.name, cd) for cd in cols])

    @classmethod
    def config_fields(cls):

        tags = ['inline_config']

        return collections.OrderedDict([
            ('local_checksum', form.BooleanField('Perform local checksum:',
                                                 default_value=True)),
            ('max_xfer_threads',
             form.IntegerField('Maximum number of transfer threads:',
                               default_value='16')),
            ('use_irods_env', form.BooleanField('Use irods environment file:',
                                                disables_tags=tags)),
            ('host', form.HostnameField('iRODS host:', tags=tags)),
            ('port', form.IntegerField('iRODS port:', '1247', tags=tags)),
            ('zone', form.TextField('iRODS zone:', tags=tags)),
            ('user_name', form.TextField('iRODS user name:', tags=tags)),
            ('default_resc', form.TextField('Default resource:', tags=tags)),
            ('store_password', form.BooleanField('Remember password:',
                                                 enables_tags=['password'],
                                                 tags=tags)),
            ('password', form.PasswordField('iRODS password:',
                                            encode=cls.encode,
                                            decode=cls.decode,
                                            tags=tags + ['password'])),
        ])


class iRODSCatalog3(iRODSCatalogBase):
    """
    A Catalog for connecting to iRODS v3
    """

    def __init__(self, host, port, user, zone, scrambled_password,
                 default_resc, local_checksum, xfer_nt):
        try:
            password = iRODSCatalogBase.decode(scrambled_password)
            session = iRODSSession(host=host, port=port, user=user,
                                   password=password, zone=zone,
                                   default_hash_scheme='MD5')
        except irods.exception.CAT_INVALID_AUTHENTICATION as e:
            raise exceptions.ConnectionError(e)

        super(iRODSCatalog3, self).__init__(session, default_resc,
                                            local_checksum, xfer_nt)


class iRODSCatalog4(iRODSCatalogBase):
    """
    A Catalog for connecting to iRODS v4
    """

    @classmethod
    def from_env_file(cls, env_file, local_checksum):
        session = iRODSSession(irods_env_file=env_file)

        return cls(session, None, local_checksum, 16)

    @classmethod
    def from_options(cls, host, port, user, zone, scrambled_password,
                     default_resc, local_checksum, default_hash_scheme,
                     xfer_nt, ssl_settings=None):
        kwargs = {}
        try:
            password = iRODSCatalogBase.decode(scrambled_password)
            kwargs.update(dict(host=host, port=port, user=user,
                               password=password, zone=zone,
                               default_hash_scheme=default_hash_scheme))
        except irods.exception.CAT_INVALID_AUTHENTICATION as e:
            raise exceptions.ConnectionError(e)

        if ssl_settings is not None:
            kwargs.update(ssl_settings)

        session = iRODSSession(**kwargs)

        return cls(session, default_resc, local_checksum, xfer_nt)

    @classmethod
    def config_fields(cls):
        base_dict = iRODSCatalogBase.config_fields()

        tags = base_dict['host'].tags

        base_dict.update({
            ('irods_default_hash_scheme',
             form.RadioChoiceField('Default hash scheme',
                                   values=['MD5', 'SHA256'],
                                   default_value='SHA256',
                                   tags=tags)),
        })

        ssl_tag = 'ssl_config'

        ssl_tags = tags + [ssl_tag]

        ssl_options = collections.OrderedDict([
            ('irods_client_server_policy',
             form.RadioChoiceField('irods_client_server_policy',
                                   values=['CS_NEG_REQUIRE', 'CS_NEG_REFUSE',
                                           'CS_NEG_DONT_CARE'],
                                   default_value='CS_NEG_REQUIRE',
                                   tags=tags)),

            ('use_irods_ssl', form.BooleanField('Use irods SSL transfer',
                                                enables_tags=[ssl_tag],
                                                tags=tags)),
            ('irods_encryption_algorithm',
             form.TextField('irods_encryption_algorithm:',
                            default_value='AES-256-CBC', tags=ssl_tags)),
            ('irods_encryption_key_size',
             form.IntegerField('irods_encryption_key_size:', default_value='32',
                               tags=ssl_tags)),
            ('irods_encryption_num_hash_rounds',
             form.IntegerField('irods_encryption_num_hash_rounds:',
                               default_value='16', tags=ssl_tags)),
            ('irods_encryption_salt_size',
             form.IntegerField('irods_encryption_salt_size:', default_value='8',
                               tags=ssl_tags)),
            ('irods_ssl_ca_certificate_file',
             form.FileSelectorField('irods_ssl_ca_certificate_file:',
                                    tags=ssl_tags)),
        ])

        base_dict.update(ssl_options)

        return base_dict


def irods3_catalog_from_envfile(envfile, local_checksum, xfer_nt):
    """
    Creates an iRODSCatalog from a iRODS v3 configuration file (like
    "~/.irods/.irodsEnv")
    """
    env3 = parse_env3(envfile)

    host = env3['irodsHost']
    port = int(env3.get('irodsPort', '1247'))
    user = env3['irodsUserName']
    zone = env3['irodsZone']
    pwdfile = env3['irodsAuthFileName']
    default_resc = env3.get('irodsDefResource', None)

    with open(pwdfile, 'r') as f:
        scrambled_password = f.read().strip()

    return iRODSCatalog3(host, port, user, zone, scrambled_password,
                         default_resc, local_checksum, xfer_nt)


def irods3_catalog_from_config(cfg):
    """
    Creates an iRODSCatalog from configuration
    """
    local_checksum = option_is_true(cfg.get('local_checksum', 'True'))
    xfer_nt = int(cfg.get('max_xfer_threads', '16'))
    use_env = option_is_true(cfg['use_irods_env'])

    if use_env:
        envfile = os.path.join(os.path.expanduser('~'), '.irods', '.irodsEnv')
        return lambda master: irods3_catalog_from_envfile(envfile,
                                                          local_checksum, xfer_nt)

    host = cfg['host']
    port = cfg['port']
    user = cfg['user_name']
    zone = cfg['zone']

    default_resc = cfg.get('default_resc', None)
    if default_resc == '':
        # empty string is not valid for default_resc
        default_resc = None

    store_password = cfg['store_password']
    scrambled_password = None
    if option_is_true(store_password):
        scrambled_password = cfg['password']
        return lambda master: iRODSCatalog3(host, port, user, zone,
                                            scrambled_password, default_resc,
                                            local_checksum, xfer_nt)
    else:
        def ask_password(master):
            cancelled = {'cancelled': False}

            def _do_ok(e=None):
                tl.destroy()

            def _do_cancel(e=None):
                pf.from_string('')
                cancelled['cancelled'] = True
                tl.destroy()

            tl = tk.Toplevel(master)
            tl.title('iRODS password')
            tl.transient(master)

            ff = form.FormFrame(tl)
            pf = form.PasswordField('password for {}@{}:'.format(user, zone),
                                    return_cb=_do_ok)
            ff.grid_fields([pf])
            ff.pack()

            butbox = tk.Frame(tl)
            butbox.pack()
            ok = tk.Button(butbox, text='Ok', command=_do_ok)
            ok.grid()
            ok.bind('<Return>', _do_ok)
            cancel = tk.Button(butbox, text='Cancel', command=_do_cancel)
            cancel.grid(row=0, column=1)
            cancel.bind('<Return>', _do_cancel)

            tl.wait_window()

            if cancelled['cancelled']:
                return None

            scrambled_password = iRODSCatalogBase.encode(pf.to_string())

            return iRODSCatalog3(host, port, user, zone, scrambled_password,
                                 default_resc, local_checksum, xfer_nt)

        return ask_password


def irods4_catalog_from_config(cfg):
    """
    Creates an iRODSCatalog from configuration
    """
    local_checksum = option_is_true(cfg.get('local_checksum', 'True'))
    xfer_nt = int(cfg.get('max_xfer_threads', '16'))
    use_env = option_is_true(cfg['use_irods_env'])

    if use_env:
        envfile = os.path.join(os.path.expanduser('~'), '.irods',
                               'irods_environment.json')
        return lambda master: iRODSCatalog4.from_env_file(envfile,
                                                          local_checksum)

    host = cfg['host']
    port = cfg['port']
    user = cfg['user_name']
    zone = cfg['zone']

    default_hash_scheme = cfg['irods_default_hash_scheme']

    ssl = None
    if option_is_true(cfg['use_irods_ssl']):
        ssl = {
            'irods_client_server_negotiation': 'request_server_negotiation',
            'irods_client_server_policy': cfg['irods_client_server_policy'],
            'irods_encryption_algorithm': cfg['irods_encryption_algorithm'],
            'irods_encryption_key_size': int(cfg['irods_encryption_key_size']),
            'irods_encryption_num_hash_rounds':
                int(cfg['irods_encryption_num_hash_rounds']),
            'irods_encryption_salt_size':
                int(cfg['irods_encryption_salt_size']),
            'irods_ssl_ca_certificate_file':
                cfg['irods_ssl_ca_certificate_file'],
        }

    default_resc = cfg.get('default_resc', None)
    if default_resc == '':
        # empty string is not valid for default_resc
        default_resc = None

    store_password = cfg['store_password']
    scrambled_password = None
    if option_is_true(store_password):
        scrambled_password = cfg['password']
        return lambda master: iRODSCatalog4.from_options(host, port, user,
                                                         zone,
                                                         scrambled_password,
                                                         default_resc,
                                                         local_checksum,
                                                         default_hash_scheme,
                                                         xfer_nt,
                                                         ssl)
    else:
        def ask_password(master):
            cancelled = {'cancelled': False}

            def _do_ok(e=None):
                tl.destroy()

            def _do_cancel(e=None):
                pf.from_string('')
                cancelled['cancelled'] = True
                tl.destroy()

            tl = tk.Toplevel(master)
            tl.title('iRODS password')
            tl.transient(master)

            ff = form.FormFrame(tl)
            pf = form.PasswordField('password for {}@{}:'.format(user, zone),
                                    return_cb=_do_ok)
            ff.grid_fields([pf])
            ff.pack()

            butbox = tk.Frame(tl)
            butbox.pack()
            ok = tk.Button(butbox, text='Ok', command=_do_ok)
            ok.grid()
            ok.bind('<Return>', _do_ok)
            cancel = tk.Button(butbox, text='Cancel', command=_do_cancel)
            cancel.grid(row=0, column=1)
            cancel.bind('<Return>', _do_cancel)

            tl.wait_window()

            if cancelled['cancelled']:
                return None

            scrambled_password = iRODSCatalogBase.encode(pf.to_string())

            return iRODSCatalog4.from_options(host, port, user, zone,
                                              scrambled_password, default_resc,
                                              local_checksum,
                                              default_hash_scheme,
                                              xfer_nt, ssl)

        return ask_password
