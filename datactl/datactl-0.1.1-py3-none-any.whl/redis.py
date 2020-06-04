import json

from termcolor import colored, cprint

from datactl.utils import (
    abort, confirm, prepare_data, show_data, to_list_of_dict, dry_run)


class Redis():

    def __init__(self, obj):
        self._obj = obj

    def _get_client(self, force=False):
        cprint('URI=<%s>' % self._obj._uri)
        cprint('queue=%s database=%s' % (self._obj._queue, self._obj._database))
        cprint('size=%s offset=%s limit=%s timeout=%s seconds' %
               (self._obj._size, self._obj._offset, self._obj._limit, self._obj._timeout))
        if not force and not confirm(self._obj):
            abort()
        import redis
        return redis.Redis.from_url(self._obj._uri, db=self._obj._database)

    def create(self, msg="", size=None):
        '''
        publish some data to the list
        '''
        self._obj._size = abs(size if size is not None else self._obj._size)
        msgs = prepare_data(str(msg), self._obj)
        dry_run(msgs, self._obj)
        r = self._get_client()
        for msg in msgs: # pylint: disable=R1704
            r.lpush(self._obj._queue, json.dumps(msg))
        cprint(colored('%s item(s) published !' % len(msgs), color='green'))

    def ping(self):
        '''
        ping the server
        '''
        r = self._get_client(force=True)
        cprint(colored('ping = %s ' % r.ping(), color='green'))

    def count(self):
        '''
        count items in the list
        '''
        r = self._get_client(force=True)
        cprint(colored('count = %s' % r.llen(self._obj._queue), color='green'))

    def purge(self):
        '''
        purge a list
        '''
        r = self._get_client(force=True)
        r.delete(self._obj._queue)
        cprint(colored('purged !', color='green'))

    def require(self, size=None):
        '''
        require a number of items in the list
        '''
        self._obj._size = abs(size if size is not None else self._obj._size)
        r = self._get_client(force=True)
        count = r.llen(self._obj._queue)
        idx_to_delete = count - self._obj._size
        if idx_to_delete > 0:
            r.ltrim(self._obj._queue, 1, -idx_to_delete)
        if idx_to_delete < 0:
            self.create(size=abs(idx_to_delete))
        cprint(colored('done !', color='green'))

    def show(self):
        '''
        show list items
        '''
        r = self._get_client(force=True)
        data = []
        for item in r.lrange(self._obj._queue, self._obj._offset, self._obj._offset + self._obj._limit):
            try:
                data.append(json.loads(item))
            except:
                data.append(dict(value=item))
        data = to_list_of_dict(data)
        show_data(data, self._obj)
        cprint(colored('done !', color='green'))
