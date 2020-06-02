import json
import uuid

import pika
from pika.exceptions import AMQPConnectionError, ProbableAuthenticationError


class ConnectionStore:
    def __init__(self, callback):
        self.store = {}
        self.callback = callback

    def add(self, key, name, value, status, call_procedure, reply_to):

        if not (key in self.store):
            self.store[key] = {"params": {}, "files": {}}

        if name == 'params':
            self.store[key]['params'] = json.loads(value)
        else:
            self.store[key]['files'][name] = value

        if status == 'finished':
            self.on_request_complete(self.store.pop(key), key, call_procedure, reply_to)

    def on_request_complete(self, params, key, call_procedure, reply_to):
        self.callback(params, key, call_procedure, reply_to)


class Response:

    def __init__(self, channel, correlation_id, reply_to, params=None, files=None):

        if params is None:
            params = dict()
        self.params = params

        if files is None:
            files = dict()
        self.files = files

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self):

        keys = self.files.keys()

        if len(keys):
            status = 'sending'
        else:
            status = 'finished'

        # сначала отправляем файлы
        self.channel.basic_publish(exchange='', routing_key=self.reply_to,
                                   properties=pika.BasicProperties(correlation_id=self.correlation_id, headers={
                                       'request_status': status,
                                       'batch_name': 'params',
                                   }),
                                   body=str(self.params))

        # теперь высылаем файлы
        for i, (file_name, file_content) in enumerate(self.files.items()):
            if len(keys) - 1 == i:
                status = 'finished'
            else:
                status = 'sending'

            self.channel.basic_publish(exchange='', routing_key=self.reply_to,
                                       properties=pika.BasicProperties(correlation_id=self.correlation_id, headers={
                                           'request_status': status,
                                           'batch_name': file_name,
                                       }),
                                       body=file_content)


class Request:

    def __init__(self, channel, correlation_id, reply_to, params=None, files=None):

        if params is None:
            params = dict()
        self.params = params

        if files is None:
            files = dict()
        self.files = files

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self, name):

        keys = self.files.keys()

        if len(keys):
            status = 'sending'
        else:
            status = 'finished'

        # сначала отправляем файлы
        print()
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                   properties=pika.BasicProperties(correlation_id=self.correlation_id,
                                                                   reply_to=self.reply_to,
                                                                   headers={
                                                                       'request_status': status,
                                                                       'batch_name': 'params',
                                                                       'call_procedure': name
                                                                   }),
                                   body=str(json.dumps(self.params)))

        # теперь высылаем файлы
        for i, (file_name, file_content) in enumerate(self.files.items()):
            if len(keys) - 1 == i:
                status = 'finished'
            else:
                status = 'sending'

            self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                       properties=pika.BasicProperties(correlation_id=self.correlation_id,
                                                                       reply_to=self.reply_to,
                                                                       headers={
                                                                           'request_status': status,
                                                                           'batch_name': file_name,
                                                                           'call_procedure': name
                                                                       }),
                                       body=file_content)


class RpcServer:

    def __init__(self, host='localhost', port=5672, username='guest', password='guest', procedures=None):
        if procedures is None:
            procedures = dict()
        self.procedures = procedures
        self.connection = None
        self.channel = None
        self.connect(host, port, username, password)
        self.create_req_channel()
        self.store = ConnectionStore(self.on_complete_callback)
        self.listen()

    def connect(self, host, port, username, password):
        print('Rpc server connects to the queue server')
        credentials = pika.PlainCredentials(username=username, password=password)
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, port=port, credentials=credentials))

        except ProbableAuthenticationError:
            raise RuntimeError('Ошибка авторизации, code 1')

        except AMQPConnectionError:
            raise RuntimeError('Ошибка подключения, code 2')

    def create_req_channel(self):
        # обработать исключения
        print('Rpc server creates a channel')
        channel = self.connection.channel()
        channel.queue_declare(queue='rpc_queue')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_message)
        self.channel = channel

    def listen(self):
        # обработать исключения
        print('Listening')
        self.channel.start_consuming()

    def on_message(self, ch, method, props, body):

        request_status = props.headers["request_status"]
        batch_name = props.headers["batch_name"]
        correlation_id = props.correlation_id
        reply_to = props.reply_to
        call_procedure = props.headers["call_procedure"]
        self.on_request(request_status, batch_name, correlation_id, reply_to, call_procedure, body)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def on_complete_callback(self, params, key, call_procedure, reply_to):
        out, files = self.procedures[call_procedure](params["params"], params["files"])
        response = Response(self.channel, key, reply_to, json.dumps(out), files)
        response.send()

    # код приема запроса
    def on_request(self, request_status, batch_name, correlation_id, reply_to, call_procedure, body):
        self.store.add(correlation_id, batch_name, body, request_status, call_procedure, reply_to)


class RpcConnector:
    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.store = ConnectionStore(self.on_complete_callback)
        self.connect(host, port, username, password)
        self.create_channel()

    def connect(self, host, port, username, password):
        print('Rpc client connects to the queue server')
        credentials = pika.PlainCredentials(username=username, password=password)
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, port=port, credentials=credentials))

        except ProbableAuthenticationError:
            raise RuntimeError('Ошибка авторизации, code 1')

        except AMQPConnectionError:
            raise RuntimeError('Ошибка подключения, code 2')

    def create_channel(self):
        # обработать исключения
        print('Rpc client creates a channel')
        channel = self.connection.channel()
        self.channel = channel
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_message,
            auto_ack=True)

    def on_message(self, ch, method, props, body):
        correlation_id = props.correlation_id
        request_status = props.headers["request_status"]
        batch_name = props.headers["batch_name"]
        if self.correlation_id == correlation_id:
            self.on_response(request_status, batch_name, correlation_id, body)

    def on_complete_callback(self, params, key, call_procedure, reply_to):
        self.response = params

    def on_response(self, request_status, batch_name, correlation_id, body):
        self.store.add(correlation_id, batch_name, body, request_status, None, None)

    def call_procedure(self, name, params=None, files=None):
        if params is None:
            params = dict()
        if files is None:
            files = dict()

        request = Request(self.channel, self.correlation_id, self.callback_queue, params, files)
        request.send(name)

        while self.response is None:
            self.connection.process_data_events()

        return self.response["params"], self.response["files"]
