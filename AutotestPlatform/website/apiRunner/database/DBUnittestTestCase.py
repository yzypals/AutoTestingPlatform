#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from ..common.log import logger
from ..common.globalvar import db_related_to_project_dic
from ..unittesttestcase import MyUnittestTestCase

__all__ = ['DBUnittestTestCase']

class DBUnittestTestCase(MyUnittestTestCase):
    def test_select_one_record(self):
        if self.input_params != '':
            self.input_params = self.input_params + ','
            self.input_params = eval(self.input_params)  # 字符串类型的元组转为元组

        try:
            flag, query_result = db_related_to_project_dic[self.op_object].select_one_record(self.url_or_sql, self.input_params)
            msg = '数据库服务器返回的查询结果为为 query_result：%s, flag：%s' % (query_result, flag)
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            if flag:
                if query_result:
                    msg = '正在保存目标内容到自定义变量'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    # 如果用户自定义了“输出”参数，则还要保存目标值到用户定义的变量
                    self.save_result(query_result) # 保存查询记录
                    msg = '正在进行结果断言'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    self.assert_result(query_result)
            else:
                msg = 'fail#%s' % query_result
                self.assertEqual(1, 0, msg=msg)
        except Exception as e:
            msg = 'fail#%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)

    def test_update_record(self):
        if self.input_params != '':
            self.input_params = self.input_params
            self.input_params = eval(self.input_params)  # 字符串类型的元组转为元组

        try:
            flag, execute_result = db_related_to_project_dic[self.op_object].execute_update(self.url_or_sql, self.input_params)
            if not flag:
                msg = 'fail#%s' % execute_result
                self.assertEqual(1, 0, msg=msg)
        except Exception as e:
            msg = 'fail#%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)

    def test_delete_record(self):
        if self.input_params != '':
            self.input_params = self.input_params
            self.input_params = eval(self.input_params)  # 字符串类型的元组转为元组
        try:
            flag, execute_result = db_related_to_project_dic[self.op_object].execute_update(self.url_or_sql, self.input_params)
            if not flag:
                msg = 'fail#%s' % execute_result
                self.assertEqual(1, 0, msg=msg)
        except Exception as e:
            msg = 'fail#%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)

    def test_call_proc(self):
        if self.input_params != '':
            self.input_params = self.input_params
            self.input_params = eval(self.input_params)  # 字符串类型的元组转为元组
        try:
            flag, execute_result = db_related_to_project_dic[self.op_object].call_proc(self.url_or_sql, self.input_params)
            if not flag:
                msg = 'fail#%s' % execute_result
                self.assertEqual(1, 0, msg=msg)
        except Exception as e:
            msg = 'fail#%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)

    def test_truncate_table(self):
        if self.input_params != '':
            self.input_params = self.input_params
            self.input_params = eval(self.input_params)  # 字符串类型的元组转为元组
        try:
            flag, execute_result = db_related_to_project_dic[self.op_object].execute_update(self.url_or_sql, self.input_params)
            if not flag:
                msg = 'fail#%s' % execute_result
                self.assertEqual(1, 0, msg=msg)
        except Exception as e:
            msg = 'fail#%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)


    def test_insert_record(self):
        if self.input_params != '':
            self.input_params = self.input_params
            self.input_params = eval(self.input_params)  # 字符串类型的元组转为元组
        try:
            temp_sql = self.url_or_sql % self.input_params
            flag, execute_result = db_related_to_project_dic[self.op_object].execute_insert(temp_sql, '')
            if not flag:
                msg = 'fail#%s' % execute_result
                self.assertEqual(1, 0, msg=msg)
        except Exception as e:
            msg = 'fail#%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            self.assertEqual(1, 0, msg=msg)