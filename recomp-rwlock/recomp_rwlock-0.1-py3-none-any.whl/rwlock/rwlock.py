import logging
import os
import sys
import tempfile
import time


logger = logging.getLogger('recomp.rwlock')


class Lock(object):

    DEFAULT_TIMEOUT = 5
    DEFAULT_CHECK_INTERVAL = 0.2


    def __init__(self, filename, mode='r', timeout=DEFAULT_TIMEOUT, check_interval=DEFAULT_CHECK_INTERVAL):
        """A simple Read-Write Lock manager

        :param filename:
        :param mode:
        :param timeout:
        :param check_interval:
        """

        if check_interval is None:
            raise IllegalArgumentException("'check_interval' is not set.")

        self.readonly = Lock._is_readonly(mode)
        if self.readonly:
            self.suffix = '.r-lock'
        else:
            self.suffix = '.w-lock'

        self.mode = mode
        self.filename = os.path.abspath(filename)
        self.filehandle = None
        self.timeout = timeout
        self.check_interval = check_interval
        self.lockfile = None
        self.lockhandle = None

    def __enter__(self):
        if self.readonly:
            # To get a read lock make sure that no write locks exist on a file.
            return self._acquire('.w-lock')
        else:
            # To get a write lock make sure that no locks exists on a file.
            return self._acquire('-lock')

    def __exit__(self, type_, value, tb):
        self._release()

    def _acquire(self, lock_suffix):
        logger.debug('Entering _acquire on: ' + self.filename)

        if self.filehandle:
            return self.filehandle

        try:
            deadline = time.monotonic() + self.timeout
            prefix = os.path.basename(self.filename)
            self.lockhandle, self.lockfile = tempfile.mkstemp(self.suffix, prefix, os.path.dirname(self.filename))
            lockfile_stat = os.stat(self.lockfile)
            logger.debug('Lock file created: %s, %d', self.lockfile, lockfile_stat.st_mtime_ns)
            logger.debug('Pre lock loop: %s', self.filename)
            while Lock._exists_earlier(prefix, lock_suffix,
                                       os.path.dirname(self.lockfile), lockfile_stat):
                if time.monotonic() < deadline:
                    logger.debug('Cannot lock yet; waiting on: ' + self.filename)
                    time.sleep(self.check_interval)
                else:
                    logger.debug('Cannot lock; timeout')
                    raise TimeoutException('Cannot lock file: ' + self.filename)

            logger.debug('Pre file open: %s (%s)', self.filename, self.lockfile)
            self.filehandle = open(self.filename, self.mode)
            logger.debug('File opened: ' + self.filename)
            return self.filehandle
        except (LockException, IOError) as x:
            self._release()
            logger.exception('Cannot lock file %s: exception occured: %s', self.filename, x)
            raise x
        except:
            self._release()
            logger.critical("Unexpected error:", sys.exc_info()[0])
            raise

    def _release(self):
        if self.lockhandle:
            try:
                if self.filehandle:
                    self.filehandle.close()
                    self.filehandle = None
                os.close(self.lockhandle)
                os.remove(self.lockfile)
                self.lockhandle = None
                self.lockfile = None
                logger.debug('Lock released: ' + self.filename)
            except IOError as x:
                logger.exception('Error releasing the lock on file %s: %s', self.filename, x)

    @staticmethod
    def _exists_earlier(prefix, suffix, adir, lockstat):

        try:
            logger.debug('Entering _exists_earlier: (%s / %s * %s)', adir, prefix, suffix)
            with os.scandir(adir) as dir_it:
                for f in dir_it:
                    if f.name.startswith(prefix) and f.name.endswith(suffix):
                        if f.stat().st_mtime_ns < lockstat.st_mtime_ns:
                            return True
                        elif f.stat().st_mtime_ns == lockstat.st_mtime_ns and f.inode() < lockstat.st_ino:
                            logger.warning('(%s / %s * %s): inode tie break...', adir, prefix, suffix)
                            return True

            return False
        finally:
            logger.debug('Exiting _exists_earlier: (%s / %s * %s)', adir, prefix, suffix)


    @staticmethod
    def _is_readonly(mode):
        return not Lock.containsAny(mode, 'aw+')

    # Might be moved to some utility lib.
    @staticmethod
    def containsAny(str, chset):
        """ Returns True if string str contains any of the characters of the chset. """

        for c in chset:
            if c in str:
                return True

        return False

    # Might be moved to some utility lib.
    #@staticmethod
    #def containsAll(str, chset):
    #    """ Returns True if string str contains all of the characters of the chset. """
    #    for c in chset:
    #        if c not in str:
    #            return False
    #
    #    return True


class LockException(Exception):
    pass


class IllegalArgumentException(LockException):
    pass


class TimeoutException(LockException):
    pass
