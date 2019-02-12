#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'laifuyu'

import redis

class RedisClient:
    def __init__(self, host, port, password=None, db='0'):
        self.r = redis.StrictRedis(host=host, port=port, password=password, db=db)

    # 连接redis
    # def connect_redis(self, host, port, password=None, db='0'):
    #     self.r = redis.StrictRedis(host=host, port=port, password=password, db=db)

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

# 测试
# if __name__ == '__main__':
    # redis_client = RedisClient('10.202.40.105', 8080, 'admin.123')
    #
    # print(redis_client.set_key_value('testkey', 'testvalue'))
#
#     # 返回列表，形如 [b'testkey']，[b'ddt:pf:msg:pushed:1061805', b'req:limit:qty:reset:pwd:18110000014']
#     print(redis_client.get_keys('testke*'))
#     print(redis_client.get_keys('*18*'))
#
#     print(redis_client.get_keys('nonexists_key')) # key不存在，则返回 []
#
#     print(redis_client.get_value_of_key('testkey')) # 返回值 b'testvalue'
#
#     print(redis_client.delete_key('testkey'))
#
#     print(redis_client.get_value_of_key('testkey')) # key不存在,获取不到对应的值，返回None

myredis = RedisClient('10.202.40.105', 8080, 'admin.123')
