# -*- coding: utf-8 -*-

from kafka import KafkaProducer
from kafka import KafkaConsumer
import time


# 接收信息
def receive(topic, kafka_hosts):
    # print('进入消费者线程', datetime.time())
    consumer = KafkaConsumer(topic, enable_auto_commit=False,
                             bootstrap_servers=kafka_hosts,
                             session_timeout_ms=6000,
                             heartbeat_interval_ms=2000)

    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value.decode('utf-8'))
        print('soncumer:', recv)


# 发送信息
def send(topic, message, kafka_hosts):
    """
        发送消息至kafka
    :param topic: 主题
    :param message: 内容
    :param kafka_hosts: hosts
    """
    producer = KafkaProducer(bootstrap_servers=kafka_hosts,
                             value_serializer=lambda v: bytes(v, encoding="utf-8")
                             )

    # 调用send方法，发送名字为'kafka_topic'的topicid ，发送的消息为message_string
    producer.send(topic, message)
    producer.flush()


if __name__ == '__main__':
    import uuid
    import json

    kafka_hosts = '192.168.195.1:32400,192.168.195.1:32401,192.168.195.1:32402'
    topic = 'gmo_test_0526'

    for i in range(0, 1):
        alarm_id = str(uuid.uuid1())
        alarm_content = 'CPU密集型任务过多'
        message = {
            'alarm_id': alarm_id,
            'alarm_content': alarm_content
        }
        message = {"aiPushUrl": "http://192.168.119.27:8080/ai/callback", "taskId": "test",
                   "data": {"errorCode": 0, "message": "sucess", "data": {"taskId": "test", "timestamp": 1590481493888,
                                                                          "algResult": {"code": 0, "alarmNum": 10,
                                                                                        "location": [
                                                                                            {"x1": 579, "y1": 233,
                                                                                             "x2": 658, "y2": 496},
                                                                                            {"x1": 853, "y1": 211,
                                                                                             "x2": 954, "y2": 556},
                                                                                            {"x1": 287, "y1": 246,
                                                                                             "x2": 341, "y2": 441},
                                                                                            {"x1": 759, "y1": 255,
                                                                                             "x2": 840, "y2": 506},
                                                                                            {"x1": 510, "y1": 253,
                                                                                             "x2": 586, "y2": 472},
                                                                                            {"x1": 405, "y1": 222,
                                                                                             "x2": 460, "y2": 451},
                                                                                            {"x1": 253, "y1": 237,
                                                                                             "x2": 305, "y2": 451},
                                                                                            {"x1": 328, "y1": 248,
                                                                                             "x2": 385, "y2": 436},
                                                                                            {"x1": 674, "y1": 251,
                                                                                             "x2": 759, "y2": 492},
                                                                                            {"x1": 486, "y1": 241,
                                                                                             "x2": 525, "y2": 435}]}}}}

        message = json.dumps(message, ensure_ascii=False)
        try:
            print('发送kafaka信息，message=', message)
            send(topic, message, kafka_hosts)
        except Exception as e:
            print(e.__traceback__)
        time.sleep(1)

    print("消费kafka")
    receive(topic, kafka_hosts)
