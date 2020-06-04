# -*- coding: utf-8 -*-
# @Time: 2020/6/3 0003
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:

from aibase.middleware import redis_util as _local_redis

redis_conn = _local_redis.redis_conn
set_redis = _local_redis.set_redis

from aibase.middleware import kafka_util as _local_redis

kafka_send = _local_redis.send
