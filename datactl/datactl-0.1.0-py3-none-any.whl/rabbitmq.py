import json

from termcolor import colored, cprint

from datactl.utils import (
    abort, confirm, prepare_data, show_data, to_list_of_dict, dry_run)


class RabbitMQ():

    def __init__(self, obj):
        self._obj = obj

    def _get_client(self, force=False):
        cprint('URI=<%s>' % self._obj._uri)
        cprint('queue=%s' % self._obj._queue)
        cprint('size=%s offset=%s limit=%s timeout=%s seconds' %
               (self._obj._size, self._obj._offset, self._obj._limit, self._obj._timeout))
        if not force and not confirm(self._obj):
            abort()
        import pika
        parameters = pika.URLParameters(self._obj._uri)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue = channel.queue_declare(
            queue=self._obj._queue, durable=True, exclusive=False, auto_delete=False)
        return connection, channel, queue

    def create(self, msg="", size=None):
        # pylint: disable=R1704
        '''
        publish some data to the queue
        '''
        self._obj._size = abs(size if size is not None else self._obj._size)
        msgs = prepare_data(str(msg), self._obj)
        dry_run(msgs, self._obj)
        connection, channel, _ = self._get_client()
        for msg in msgs:
            channel.basic_publish(
                exchange=self._obj._exchange,
                routing_key=self._obj._routing_key or self._obj._queue,
                body=json.dumps(msg))
        connection.close()
        cprint(colored('%s item(s) published !' % len(msgs), color='green'))

    def ping(self):
        '''
        ping the server
        '''
        connection, channel, _ = self._get_client(force=True)
        cprint(colored('connection.is_open = %s ' %
                       connection.is_open, color='green'))
        cprint(colored('channel.is_open = %s ' %
                       channel.is_open, color='green'))
        connection.close()

    def count(self):
        '''
        count items in the queue
        '''
        connection, _, queue = self._get_client(force=True)
        cprint(colored('count = %s' % queue.method.message_count, color='green'))
        connection.close()

    def purge(self):
        '''
        purge a queue
        '''
        connection, channel, _ = self._get_client(force=True)
        channel.queue_purge(self._obj._queue)
        connection.close()
        cprint(colored('purged !', color='green'))

    def require(self, size=None):
        '''
        require a number of messages in the queue
        '''
        self._obj._size = abs(size if size is not None else self._obj._size)
        connection, channel, queue = self._get_client(force=True)
        count = queue.method.message_count
        idx_to_delete = count - self._obj._size
        i = 0
        if idx_to_delete > 0:
            for method_frame, _, _ in channel.consume(self._obj._queue, inactivity_timeout=1, auto_ack=False):
                if not method_frame:
                    break
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                i += 1
                if i == idx_to_delete:
                    break
        if idx_to_delete < 0:
            self.create(size=abs(idx_to_delete))
        cprint(colored('done !', color='green'))
        connection.close()

    def show(self):
        '''
        show messages from a queue
        '''
        connection, channel, _ = self._get_client(force=True)
        data = []
        i = 0
        for method_frame, _, body in channel.consume(self._obj._queue, inactivity_timeout=1, auto_ack=False):
            i += 1
            if not method_frame:
                break
            if i < self._obj._offset:
                continue
            if i == (self._obj._limit + self._obj._offset):
                break
            try:
                data.append(json.loads(body))
            except:
                data.append(dict(value=body))
        connection.close()
        data = to_list_of_dict(data)
        show_data(data, self._obj)
        cprint(colored('done !', color='green'))
