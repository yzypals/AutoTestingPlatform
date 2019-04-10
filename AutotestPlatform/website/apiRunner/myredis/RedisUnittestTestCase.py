#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'


from ..common.log import logger
from ..unittesttestcase import MyUnittestTestCase
from ..common.globalvar import redis_related_to_project_dic


__all__ = ['RedisUnittestTestCase']

class RedisUnittestTestCase(MyUnittestTestCase):
    def test_set_key_value(self):
        '''存储键值'''
        try:
            self.input_params = self.input_params.replace('，', ',').strip()
            arg_list = self.input_params.split(',')
            if len(arg_list) < 2:
                self.assertEqual(1, 0, '参数填写错误(合法参数格式：key,value)，参数：%s' % self.input_params)
                return
            else:
                key = arg_list[0].strip()
                value = arg_list[1].strip()

            result = redis_related_to_project_dic[self.op_object].set_key_value(key, value)
            if result:
                logger.info('存储键值成功')
            else:
                msg = 'fail#%存储键值失败'
                self.assertEqual(1, 0, msg=msg)
        except Exception as e:
            msg = 'fail#存储键值失败%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)




