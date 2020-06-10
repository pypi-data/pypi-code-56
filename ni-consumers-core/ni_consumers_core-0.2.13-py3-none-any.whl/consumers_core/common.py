import pika


def extract_informations(headers):
    params = headers['params'] if 'params' in headers else None
    operations = headers['operations'] if 'operations' in headers else None
    pipeline_id = headers['pipeline_id']
    step_id = headers['step_id']
    name = headers['name']
    extension = headers['extension']

    return params, operations, pipeline_id, step_id, name, extension


def resend(body, params, pipeline_id, step_id, consumer_id, status, reason, name, extension, amqp_url, amqp_port=5672):

    headers = {'pipeline_id': pipeline_id, 'step_id': step_id, 'consumer_id': consumer_id, 'status': status,
               'reason': reason, 'name': name, 'extension': extension, 'params': params}

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('10.0.0.8', amqp_port, '/', credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='job-finish', durable=True,
                          arguments={'x-dead-letter-exchange': '',
                                   'x-dead-letter-routing-key': 'job-finish.dead-letter.queue'})

    channel.basic_publish(exchange='',
                          routing_key='job-finish',
                          properties=pika.BasicProperties(
                              headers=headers
                          ),
                          body=body)

    connection.close()
    """with open(f"{name}.{extension}", "wb") as image:
        image.write(body)

    with open(f"{name}.{extension}", "rb") as image:
        files = {"media": image}
        content = {"pipeline_id": pipeline_id, "step_id": step_id, "consumer_id": consumer_id, "params": params}
        if reason:
            content['reason'] = reason

        data = {"data": [content]}
        # requests.post(url, files=files, data=data)"""
