#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import configparser
import sys
import os
import mysql.connector

from ..common.log import logger

class MyDB:
    """动作类，获取数据库连接，配置数据库IP，端口等信息，获取数据库连接"""

    def __init__(self, log_websocket_consumer, db='', db_name='', db_host='', port=3306, user='', password='', charset='utf8'):
        if db:
            config = configparser.ConfigParser()
            # 从配置文件中读取数据库服务器IP、域名，端口

            co_filepath = sys._getframe().f_code.co_filename
            head, tail = os.path.split(co_filepath)
            conf_filepath = os.path.join(head, '../conf/db.conf')
            conf_filepath = os.path.normpath(conf_filepath)

            config.read(conf_filepath, encoding='utf-8')
            self.host = config[db]['host']
            self.port = config[db]['port']
            self.user = config[db]['user']
            self.passwd = config[db]['passwd']
            self.db_name = config[db]['db']
            self.charset = config[db]['charset']
        else:
            self.host = db_host
            self.port = port
            self.user = user
            self.passwd = password
            self.db_name = db_name
            self.charset = charset
        self.log_websocket_consumer = log_websocket_consumer # 输出日志到web页面使用

        try:
            self.dbconn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.db_name, charset=self.charset)
        except Exception as e:
            msg = '初始化数据连接失败：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            sys.exit(1)

    def get_host(self):
        return self.host


    def get_port(self):
        return self.port

    def get_conn(self):
        return self.dbconn

    def execute_create(self,query):
        msg = 'query：%s' % query
        logger.info(msg)
        self.log_websocket_consumer.info(msg)
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            db_cursor.execute('commit')
            db_cursor.close()
            return True
        except Exception as e:
            msg = '创建数据库表操作失败：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit(1)

    def execute_insert(self, query, data):
        query = query.replace('"', "'")
        msg = 'query：%s  data：%s' % (query, data)
        logger.info(msg)
        self.log_websocket_consumer.info(msg)
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query, data)
            db_cursor.execute('commit')
            db_cursor.close()
            return [True, '']
        except Exception as e:
            msg = '执行数据库插入操作失败：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            db_cursor.execute('rollback')
            db_cursor.close()
            return [False, '%s'% e]

    def execute_update(self, query, data):
        if data:
            query = query % data
        msg = 'update_query：%s' % query
        logger.info(msg)
        self.log_websocket_consumer.info(msg)
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            db_cursor.execute('commit')
            db_cursor.close()
            return [True, '']
        except Exception as e:
            msg = '执行数据库更新操作失败：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            db_cursor.execute('rollback')
            db_cursor.close()
            return [False, '%s'% e]
        
    def call_proc(self, query, data):
        if data:
            query = query % data
        logger.info('call proc：%s' % query)
        try:
            db_cursor = self.dbconn.cursor()
            for result in db_cursor.execute(query, multi=True):
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(
                        result.statement))
                    result.fetchall()
                    # print(result.fetchall())
                else:
                    pass
                    # print("Number of rows affected by statement '{}': {}".format(
                    #     result.statement, result.rowcount))
            db_cursor.execute('commit')
            db_cursor.close()
            return [True, '']
        except Exception as e:
            msg = '执行数据库更新操作失败：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            db_cursor.execute('rollback')
            db_cursor.close()
            return [False, '%s'% e]

    def select_one_record(self, query, data=""):
        '''返回结果只包含一条记录'''
        logger.info('query：%s  data：%s' % (query, data))
        if data:
            query = query.replace('"', "'") % data
        msg = '执行的查询语句为：%s' % query
        logger.info(msg)
        self.log_websocket_consumer.info(msg)
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            query_result = db_cursor.fetchall()
            if query_result:
                query_result = query_result[0]

            temp_list = []
            for item in query_result:
                if type(item) == type(bytearray(b'')): # 转换字节数组为字符串
                    item = item.decode('utf-8')
                temp_list.append(item)
            query_result = temp_list
            self.dbconn.commit()
            db_cursor.close()
            return (True, query_result)
        except Exception as e:
            msg = '执行数据库查询操作失败：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            db_cursor.close()
            return [False, '%s'% e]




    def select_many_record(self, query, data=""):
        '''返回结果包含多条记录'''
        logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            if data:
                db_cursor.execute(query, data)
            else:
                db_cursor.execute(query)
            query_result = db_cursor.fetchall()
            final_result = []
            for record  in query_result:
                temp_result = []
                for item in record:
                    if type(item) == type(bytearray(b'')): # 转换字节数组为字符串类型
                        item = item.decode('utf-8')
                    temp_result.append(item)
                final_result.append(temp_result)
            query_result = final_result
            self.dbconn.commit()
            db_cursor.close()
            return [True,query_result]
        except Exception as e:
            logger.error('执行数据库查询操作失败：%s' % e)
            db_cursor.close()
            return [False, '%s'% e]

    def close(self):
        self.dbconn.close
