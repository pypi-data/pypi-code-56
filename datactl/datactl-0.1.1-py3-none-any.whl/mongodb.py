from pprint import pformat

from termcolor import colored, cprint

from datactl.utils import (
    abort, confirm, prepare_data, show_data, to_list_of_dict, dry_run)


class MongoDB():

    def __init__(self, obj):
        self._obj = obj

    def _get_client(self, force=False, with_collection=True, with_database=True):
        cprint('URI=<%s>' % self._obj._uri)
        cprint('collection=%s database=%s' %
               (self._obj._collection, self._obj._database))
        cprint('size=%s offset=%s limit=%s timeout=%s seconds' %
               (self._obj._size, self._obj._offset, self._obj._limit, self._obj._timeout))
        if not force and not confirm(self._obj):
            abort()
        from pymongo import MongoClient
        client = MongoClient(
            self._obj._uri, connectTimeoutMS=self._obj._timeout*1000)
        if with_collection:
            client = client[self._obj._collection]
            if with_database:
                client = client[self._obj._database]
        return client

    def create(self, msg="", size=None):
        '''
        publish some data to the database
        '''
        self._obj._size = abs(size if size is not None else self._obj._size)
        msgs = prepare_data(str(msg), self._obj)
        dry_run(msgs, self._obj)
        db = self._get_client()
        res = db.insert_many(msgs)
        cprint(colored('%s item(s) are published !' %
                       len(res.inserted_ids), color='green'))

    def ping(self):
        '''
        ping the database
        '''
        db = self._get_client(force=True, with_collection=False)
        cprint(colored('result = %s ' %
                       pformat(db.admin.command('ping')), color='green'))

    def count(self):
        '''
        count items in the database
        '''
        db = self._get_client()
        cprint(colored('count = %s' % db.count_documents({}), color='green'))

    def purge(self):
        '''
        purge a mongo database
        '''
        db = self._get_client()
        db.delete_many({})
        cprint(colored('purged !', color='green'))

    def require(self, size=None):
        '''
        require a number of documents in the database
        '''
        self._obj._size = abs(size if size is not None else self._obj._size)
        db = self._get_client()
        count = db.count_documents({})
        idx_to_delete = count - self._obj._size
        for _ in range(idx_to_delete):
            db.delete_one({})
        if idx_to_delete < 0:
            self.create(size=abs(idx_to_delete))
        cprint(colored('new size=%s' % db.count_documents({}), color='green'))

    def show(self):
        '''
        Show documents from the database
        '''
        db = self._get_client(force=True)
        data = db.find().skip(self._obj._offset).limit(self._obj._limit)
        data = to_list_of_dict(data)
        show_data(data, self._obj)
        cprint(colored('done !', color='green'))
