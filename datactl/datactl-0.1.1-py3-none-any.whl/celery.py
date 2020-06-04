from termcolor import colored, cprint

from datactl.utils import (abort, confirm, prepare_data, dry_run)


class Celery():

    def __init__(self, obj):
        self._obj = obj

    def _get_client(self, force=False):
        cprint('broker=<%s>' % self._obj._broker)
        cprint('backend=<%s>' % self._obj._backend)
        cprint('queue=<%s> endpoint=<%s>' %
               (self._obj._queue, self._obj._endpoint))
        cprint('exchange=<%s> routing_key=<%s>' %
               (self._obj._exchange, self._obj._routing_key))
        cprint('size=%s timeout=%s seconds' %
               (self._obj._size, self._obj._timeout))
        if not force and not confirm(self._obj):
            abort()
        from celery import Celery as Celery2
        kwargs = dict(broker=self._obj._broker)
        if self._obj._backend:
            kwargs.update(backend=self._obj._backend)
        app = Celery2(self._obj._endpoint, **kwargs)
        app.conf.task_default_queue = self._obj._queue
        if self._obj._exchange:
            app.conf.task_default_exchange = self._obj._exchange
        if self._obj._routing_key:
            app.conf.task_default_routing_key = self._obj._routing_key
        if self._obj._exchange_type:
            app.conf.task_default_exchange_type = self._obj._exchange_type
        return app

    def send(self, msg="", size=None):
        '''
        send some tasks using celery
        '''
        self._obj._size = abs(size if size is not None else self._obj._size)
        msgs = prepare_data(str(msg), self._obj)
        dry_run(msgs, self._obj)
        c = self._get_client()
        for msg in msgs:  # pylint: disable=R1704
            res = c.send_task(self._obj._endpoint, (msg, ))
            cprint(colored('ID = %s' % res, color='cyan'))
        cprint(colored('%s item(s) sent !' % len(msgs), color='green'))

    def get(self, task_id):
        '''
        get result by task ID
        '''
        from celery.result import AsyncResult
        r = self._get_client()
        res = AsyncResult(task_id, app=r)
        cprint(colored('state = %s' % res.state, color='green'))
        cprint(colored('result = %s' % res.get(), color='green'))
