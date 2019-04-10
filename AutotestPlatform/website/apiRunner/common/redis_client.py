#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import redis

class RedisClient:
    def __init__(self, log_websocket_consumer, host, port, password=None, db='0', charset='utf-8'):
        self.r = redis.StrictRedis(host=host, port=port, password=password, db=db, charset=charset)
        self.log_websocket_consumer = log_websocket_consumer

    # 连接redis
    # def connect_redis(self, host, port, password=None, db='0'):
    #     self.r = myredis.StrictRedis(host=host, port=port, password=password, db=db)

    # 存储 键-值
    def set_key_value(self, key, value):
        result = self.r.set(key, value)
        if result:
            return True
        else:
            return False

    # 获取键
    def get_keys(self, pattern='*'):
        result = self.r.keys(pattern=pattern)
        return result

    # 获取键值
    def get_value_of_key(self, key):
        result = self.r.get(key)
        return result

    # 删除key
    def delete_key(self, key):
        result = self.r.delete(key)
        if result != 1:
            return False
        elif result == 1:
            return True
