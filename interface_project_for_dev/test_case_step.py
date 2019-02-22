#!/usr/bin/env python
#-*- encoding:utf-8 -*-

__author__ = 'shouke'

import time
import re
import unittest
import json
from collections import OrderedDict

from common.log import logger

from common.globalvar import global_variable_dic
from common.globalvar import test_reporter
from httpprotocol import MyHttp

from interface.APIUnittestTestCase import *
from database.DBUnittestTestCase import *
from function.FuncUnittestTestCase import *


class TestCaseStep:
    def __init__(self, execution_num, plan_id, case_id, step_id, order, step_type, op_object, object_id, exec_operation, request_headers,
                    request_method, url_or_sql, input_params, response_to_check, check_rule, check_pattern,  output_params, protocol, host, port, global_headers):
        self.execution_num = execution_num
        self.plan_id = plan_id
        self.case_id = case_id
        self.step_id = step_id
        self.order = order
        self.step_type = step_type
        self.op_object = op_object
        self.object_id = object_id
        self.exec_operation = exec_operation.lower()
        self.request_headers = request_headers
        self.request_method = request_method
        self.url_or_sql = url_or_sql
        self.input_params = input_params
        self.response_to_check = response_to_check
        self.check_rule = check_rule.strip()
        self.check_pattern = check_pattern
        self.output_params = output_params
        self.protocol = protocol
        self.host = host
        self.port = port
        self.global_headers = global_headers
        self.http = MyHttp(protocol, host, port)
        self.func_map = {'死等待':'test_sleep'} # 存放函数中文名称及代码层函数的映射关系


    def set_check_pattern(self, check_pattern):
        self.check_pattern = check_pattern

    # 该函数用于替换动态变量（ 前端控制，参数名不能带空格
    def replace_variable(self, src_string):
        try:
            variable_list = re.findall('\$.+?\$', src_string)
            logger.info('检查到目标内容中待替换的动态变量有:%s' % variable_list)
            logger.info('已保存的全局变量有：%s' % global_variable_dic)
            for item in variable_list:
                logger.info('正在替换动态变量：%s' % item)
                variable = str(item.strip('$').strip())
                if type(global_variable_dic[variable]) == type(1):
                    src_string = src_string.replace(item, str(global_variable_dic[variable]))
                else:
                    src_string = src_string.replace(item, global_variable_dic[variable])

            logger.info('替换动态变量后的内容：%s'% src_string)
        except Exception as e:
            logger.error('替换动态变量出错：%s' % e)
        finally:
            return  src_string

    def run(self, debug):
        try:
            # 获取开始运行时间
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            logger.info('步骤类型：%s' % self.step_type)
            logger.info('步骤操作对象：%s' % self.op_object)
            logger.info('执行操作：%s' % self.exec_operation)
            if self.step_type == '请求接口':
                if self.request_headers:
                    logger.info('正在替换“请求头”中的动态参数')
                    self.request_headers = self.replace_variable(self.request_headers)
                    self.request_headers = json.loads(self.request_headers, object_hook=OrderedDict)
                    request_headers = self.request_headers.copy()
                else:
                    request_headers = {}

                for host in self.global_headers:
                    # 判断该host下是否有全局请求头
                    host_of_interface = self.host
                    if host == host_of_interface:
                       request_headers.update(self.global_headers[host])
                self.http.set_headers(request_headers)

                class_name = self.op_object
                exec_operation = self.exec_operation
            elif self.step_type == '操作数据库':
                class_name = 'DBUnittestTestCase'
                exec_operation = 'test_' + self.exec_operation
                request_headers = ''
            elif self.step_type == '执行函数':
                class_name = 'FuncUnittestTestCase'
                exec_operation = self.func_map.get(self.op_object)
                request_headers = ''


            if self.input_params:
                logger.info('正在替换“输入参数”中的动态参数')
                self.input_params = self.replace_variable(self.input_params)

            if self.url_or_sql:
                logger.info('正在替换“URL/SQL”中的动态参数')
                self.url_or_sql = self.replace_variable(self.url_or_sql)

            if self.host:
                logger.info('正在替换“主机地址”中的动态参数')
                self.host = self.replace_variable(self.host)
                self.http.set_host(self.host)


            if self.output_params:
                self.output_params = json.loads(self.output_params) # 转为字典

            runner = unittest.TextTestRunner()
            test_step_action = unittest.TestSuite()

            test_step_action.addTest((globals()[class_name])(self.op_object, request_headers, self.request_method, self.url_or_sql, self.input_params,
                                                                 self.check_rule, self.check_pattern, self.response_to_check,
                                                                 self.output_params, self.http, self, exec_operation))
            step_run_result = runner.run(test_step_action)

            logger.debug('step_run_result：%s, errors：%s，failures：%s' % (step_run_result, step_run_result.errors, step_run_result.failures))

            if 0 != len(step_run_result.errors):
                error = step_run_result.errors[0][1]
                result = [False, '失败', error]
            elif 0 != len(step_run_result.failures):
                failure = step_run_result.failures[0][1]
                pattern = re.compile('fail#(.+)[^\s]', re.I)
                result = re.findall(pattern, failure)
                if result:
                    result = [False, '失败', result[0]]
                else:
                    result = [False, '失败', failure]
            else:
                result = [True, '成功', '']

            remark = result[2]
        except Exception as e:
            logger.error('%s' % e)
            remark = '%s' % e
            result = [False, '失败', '%s' % e]
        finally:
            if not debug:
                logger.info('======================正在记录用例步骤运行结果到测试报告-用例步骤执行明细表======================')
                if self.step_type not in ['操作数据库', '执行函数']:
                    self.input_params = self.http.get_request_param()
                    if type(self.input_params) == type(b''):
                        self.input_params = self.input_params.decode('utf-8')
                    request_headers = json.dumps(request_headers, ensure_ascii=False, indent=4)
                else:
                    self.http.protocol, self.host, self.port = '', '', ''

                if self.check_pattern:
                    self.check_pattern = "[" + json.dumps(self.check_pattern[0], ensure_ascii=False, indent=4) + "]"

                if self.output_params:
                    self.output_params = json.dumps(self.output_params, ensure_ascii=False, indent=4)

                data = (self.execution_num, self.plan_id, self.case_id, self.step_id, self.order, self.step_type, self.op_object, self.object_id, self.exec_operation,
                            self.http.protocol, self.host, self.port, request_headers, self.request_method, self.url_or_sql,
                            self.input_params, self.response_to_check, self.check_rule, self.check_pattern, self.output_params, result[1], remark, start_time, 0)
                test_reporter.insert_report_for_case_step(data)
            return  result

