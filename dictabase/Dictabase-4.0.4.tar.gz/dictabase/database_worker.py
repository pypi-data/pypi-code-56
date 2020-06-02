import time
from collections import defaultdict
import threading
import sys
import dataset
from dictabase.helpers import LoadKeys, DumpKeys, IsEmpty


class DatabaseWorker:
    # this is the only object/thread that should interact with the database

    def __init__(self):
        self._dburi = None
        self._db = None

        self._inUseQ = defaultdict(dict)  # use dict of dicts for fast lookups
        self._alreadyDeletedQ = defaultdict(dict)

        self._workerLock = threading.Lock()

        self._debug = False

    def SetDebug(self, newState):
        self._debug = newState

    def print(self, *a, **k):
        if self._debug:
            print(*a, **k)

    def RegisterDBURI(self, dburi):
        self.print('RegisterDBURI(', dburi)
        if dburi is None:
            if sys.platform.startswith('win'):
                dburi = 'sqlite:///MyDatabase.db'
            else:  # linux
                dburi = 'sqlite:////MyDatabase.db'

        self._dburi = dburi
        self._db = dataset.connect(
            self._dburi,
            engine_kwargs={'connect_args': {'check_same_thread': False}} if 'sqlite' in self._dburi else None
            # to avoid error; ProgrammingError: SQLite objects created in a thread can only be used in that ame thread.The object was created in thread id 23508 and this is thread id 640
        )

    def AddToInsertQ(self, cls, **kwargs):
        print('AddToInsertQ')

        obj = cls(**kwargs)

        with self._workerLock:
            self._db.begin()
            d = dict(obj)
            tableName = type(obj).__name__
            ID = self._db[tableName].insert(d)
            self._db.commit()

        obj['id'] = ID

        self.AddToInUseQ(obj)
        return obj

    def AddToDropQ(self, cls):
        self.print('AddToDrop(', cls)

        self._CommitAll()

        with self._workerLock:
            self._db.begin()
            tableName = cls.__name__
            self._db[tableName].drop()
            self._db.commit()

    def AddToInUseQ(self, obj):
        self.print('AddToInUseQ(', obj)
        self._inUseQ[type(obj)][obj['id']] = obj

    def AddToCommitQ(self, obj):
        self.print('AddToCommitQ(', obj)
        # this is called when there are no more references to a BaseTable() object (aka obj.__del__() is called)

        self._inUseQ[type(obj)].pop(obj['id'], None)

        alreadyDeletedObj = self._alreadyDeletedQ[type(obj)].pop(obj['id'], None)
        if alreadyDeletedObj:
            return  # dont commit this obj. its been deleted

        with self._workerLock:
            tableName = type(obj).__name__  # do this before DumpKeys
            obj = DumpKeys(obj)
            self._db.begin()
            d = dict(obj)
            self._db[tableName].upsert(d, ['id'])  # find row with matching 'id' and update it
            self._db.commit()

    def AddToDeleteQ(self, obj):
        self.print('AddToDeleteQ(', obj)
        self._CommitAll()

        with self._workerLock:
            self._db.begin()
            tableName = type(obj).__name__
            self._db[tableName].delete(**obj)
            self._db.commit()

        self._alreadyDeletedQ[type(obj)][obj['id']] = obj

    def AddToFindOneQ(self, cls, kwargs):
        self.print('AddToFindOneQ(', cls, kwargs)
        self._CommitAll()

        # self._db.begin() # dont do this

        with self._workerLock:

            tableName = cls.__name__
            tbl = self._db[tableName]
            ret = tbl.find_one(**kwargs)
            if ret:
                ret = cls(**ret)
                ret = LoadKeys(ret)
            else:
                ret = None

        self.AddToInUseQ(ret)
        return ret

    def AddToFindAllQ(self, cls, kwargs):
        self.print('FindAll(', cls, kwargs)

        self._CommitAll()

        # special kwargs
        reverse = kwargs.pop('_reverse', False)  # bool
        orderBy = kwargs.pop('_orderBy', None)  # str
        if reverse is True:
            if orderBy is not None:
                orderBy = '-' + orderBy
            else:
                orderBy = '-id'

        # do look up
        with self._workerLock:
            tableName = cls.__name__

            if len(kwargs) == 0:
                ret = self._db[tableName].all(order_by=[f'{orderBy}'])
            else:
                if orderBy is not None:
                    ret = self._db[tableName].find(
                        order_by=['{}'.format(orderBy)],
                        **kwargs
                    )
                else:
                    ret = self._db[tableName].find(**kwargs)

        # yield type-cast items one by one
        for d in ret:
            obj = cls(**d)
            obj = LoadKeys(obj)
            self.AddToInUseQ(obj)
            yield obj

    def _CommitAll(self):
        self.print('CommitAll')

        for theType in self._inUseQ:
            for obj in self._inUseQ[theType].copy().values():
                self.AddToCommitQ(obj)
