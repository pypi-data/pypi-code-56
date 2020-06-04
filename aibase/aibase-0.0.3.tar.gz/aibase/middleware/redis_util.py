# -*- coding: utf-8 -*-
# @Time: 2020/05/13
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:
from redis import ConnectionPool, StrictRedis
from werkzeug.local import Local

__local_redis_conn = Local()

__redis_conf = {
    "host": "127.0.0.1",
    "port": 6379,
}


def set_redis(key, value):
    """
        配置redis地址
    :param key:
    :param value:
    :return:
    """
    __redis_conf[key] = value


def redis_conn():
    """
    对redis的单实例进行连接操作
    :return:
    """
    try:
        redis_conn = __local_redis_conn.redis_conn
    except:
        pool = ConnectionPool(**__redis_conf)
        # 由于redis输出数据类型是bytes，所以连接配置提供decode_responses选项，可以选择直接输出str类型数据
        __local_redis_conn.redis_conn = StrictRedis(connection_pool=pool, decode_responses=True)
        redis_conn = __local_redis_conn.redis_conn
    return redis_conn


if __name__ == '__main__':
    set_redis('host', '192.168.200.50')
    set_redis('db', '0')
    print(redis_conn().keys())
