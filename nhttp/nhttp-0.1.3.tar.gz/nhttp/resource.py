from threading import Lock


class _Resource:
    def __init__(self, file):
        self.__file = file
        self._count = 0
        self._lock = Lock()

    @property
    def file(self):
        return self.__file


class ResourcePool:
    def __init__(self, pool_size=50):
        self.__size = pool_size
        self.__pool = {}
        self.__lock = Lock()

    def __clear_pool(self, max_destroy_count_value=1):
        for k, v in self.__pool.items():
            if len(self.__pool) < self.__size:
                break

            if v.count <= max_destroy_count_value:
                del self.__pool[k]

    def open(self, fpath :str, mode='r', encoding=None) -> _Resource:
        with self.__lock:
            stab = (fpath, mode)

            if stab in self.__pool:
                rc = self.__pool[stab]
                rc._count += 1

                return rc

            f = open(fpath, mode, encoding=encoding)
            res = _Resource(f)
            res._count += 1

            if len(self.__pool) > self.__size:
                self.__clear_pool()

            self.__pool[stab] = res

            return res

    def close(self, res :_Resource):
        if res not in self.__pool.values():
            return

        f = res.file
        
        if not f.closed:
            res.file.close()
        
        sig = (f.name, f.mode)

        if sig not in self.__pool:
            return

        del self.__pool[sig]

    def __str__(self):
        return '<NHTTP Resource Pool Cap = %s ResCount = %s>' % (self.__size, len(self.__pool))

    __repr__ = __str__
