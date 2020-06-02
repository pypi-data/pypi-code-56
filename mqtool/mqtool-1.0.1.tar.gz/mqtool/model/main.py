import json
import os
import threading
import time

from mqtool.kit import Kafka_consumer, Kafka_producer
# from mqtool.kit.push_metrics import IO_metrics
from mqtool.kit.tornado_server import Tornado_http
# from mqtool.model.algo_load import load_dir
from mqtool.utils import *

# algo_list = load_dir('./algorithm')
# if len(algo_list) == 0:
#     logger.info('未加载到算法模型，程序退出！')
#     exit()
# algo = algo_list[0]
## 统计算子IO指标
# input = 0
# output = 0
# input_befor = 0
# output_befor = 0
# time_differ_list = []
# data_type = ''
# algo = ''


def start():
    return {"status": "algorithm service success"}


def api(data):
    """
    处理data参数，算法运行
    :param data: dict字段类型
    :return:
    """
    if data_type == "kafka":
        if 'picture' in data:
            fdfsKey = data['picture']
            img = readfile(str(fdfsKey))
            data['img'] = img
    elif data_type == "http":
        if 'data' in data:
            img = readfrombase64(data['data'])
            del data['data']
            data['img'] = img
        if 'structure' in data:
            data['structure'] = data['structure'].replace('\"', '')
    return algo(data)


# def cron_push():
#     """
#     定时push metrics
#     :return:
#     """
#     global input, output, input_befor, output_befor,time_differ_list
#     push_addr = os.getenv("PUSHTOGATEWAY", None)
#     if push_addr is None:
#         logger.info("None pushgateway address")
#     if push_addr is not None:
#         info = "pushgateway address:" + push_addr
#         logger.info(info)
#         while True:
#             time.sleep(60)
#             IO_metrics(push_addr,input,output,input_befor,output_befor,time_differ_list)
#             input_befor,output_befor= input,output
#             time_differ_list = []



# def push_task():
#     """
#     开启新线程推送指标
#     :return:
#     """
#     try:
#         th = threading.Thread(target=cron_push)
#         th.start()
#     except:
#         logger.exception("push metrics error")

def aistart(run):
    try:
        # push_task()
        global algo
        global data_type
        algo = run
        data_type = os.getenv("DATA_TYPE", default="http")
        if data_type == "kafka":
            bootstrap_server = os.getenv("BOOTSTRAP_SERVER")
            kafkatopic = os.getenv("TOPIC")
            storage_url = os.getenv("STORAGE_URL", default="http://localhost:8888/")
            consumer = Kafka_consumer(bootstrap_servers=bootstrap_server, kafkatopic=kafkatopic,
                                      groupid=algo.__name__)
            data = consumer.read_df()
            sinktopic = os.getenv("SINKTOPIC")
            if sinktopic is not None:
                producer = Kafka_producer(bootstrap_servers=bootstrap_server, kafkatopic=sinktopic,
                                          is_json=True)
            for message in data:
                try:
                    # input += 1
                    logger.info('receive data')
                    mes = json.loads(message.decode())
                    # time_befor=time.time()
                    res = api(mes)
                    # time_after = time.time()
                    # time_differ_list.append(time_after-time_befor)
                    if res is not None:
                        if isinstance(res, list):
                            for item in res:
                                if sinktopic is not None:
                                    producer.send_df(item)
                                http_post(storage_url, item)
                                # output +=1
                        else:
                            if sinktopic is not None:
                                producer.send_df(res)
                            http_post(storage_url, res)
                            # output += 1
                except:
                    logger.exception("deal data error")

        elif data_type == "http":
            tornado_server = Tornado_http()
            # 添加路由
            tornado_server.add_handler("/", start)
            # 数据为json格式
            tornado_server.add_handler("/predict", api, json_type=True, get=False)
            # 开启服务
            tornado_server.start_http_server()
    except:
        logger.exception("system error")
