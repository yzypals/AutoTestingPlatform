#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time

from common.log import logger
from common.globalvar import test_reporter
from common.globalvar import test_platform_db
from test_case_step import TestCaseStep


class TestCase:
    def __init__(self, execution_num, plan_id, case_id, case_path, case_name, protocol, host, port, global_headers):
        self.execution_num = execution_num
        self.plan_id = plan_id
        self.case_id = case_id
        self.case_path = case_path
        self.case_name = case_name
        self.protocol = protocol
        self.host = host
        self.port = port
        self.global_headers = global_headers

    def run(self, debug):
        try:
            # 获取开始运行时间
            timestamp_for_start = time.time()
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            logger.info('正在查询测试用例[ID：%s, 名称：%s]关联的测试步骤' % (self.case_id, self.case_name))
            query = 'SELECT id, `order`, step_type, op_object, object_id, exec_operation, request_header, request_method, url_or_sql, input_params, ' \
                    'response_to_check, check_rule, check_pattern,  output_params, protocol, host, port ' \
                    'FROM `website_api_test_case_step`  WHERE case_id=%s AND  status=\'启用\' ORDER BY `order` ASC'
            data = (self.case_id,)
            result = test_platform_db.select_many_record(query, data)

            if result[0] and result[1]:
                records = result[1]
                logger.info('开始执行测试步骤')

                result = [False, '阻塞', '没有找到与用例关联的测试步骤']
                for record in records:
                    step_id, order, step_type, op_object, object_id, exec_operation, request_header, \
                    request_method, url_or_sql, input_params, response_to_check, check_rule, \
                    check_pattern,  output_params, protocol, host, port = record
                    if protocol != '':
                        protocol = protocol
                    else:
                        protocol = self.protocol
                    if host != '':
                        host = host
                    else:
                        host = self.host
                    if port != '':
                        port = port
                    else:
                        port = self.port

                    if step_type == '执行用例':
                        # 获取开始运行时间
                        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        level_list = op_object.split('->') # op_object即为case_path
                        case_name = level_list[len(level_list) - 1]
                        test_case = TestCase(self.execution_num, self.plan_id, object_id, op_object, case_name, self.protocol, self.host, self.port, self.global_headers)
                        logger.info('======================开始运行测试步骤[第 %s 步, 步骤ID: %s]======================' % (order, step_id))
                        logger.info('步骤类型：执行用例')
                        logger.info('步骤操作对象：%s, ID：%s' % (op_object, object_id))
                        result = test_case.run(debug)

                        if not debug:
                            logger.info('======================正在记录用例步骤运行结果到测试报告-用例步骤执行明细表======================')
                            data = (self.execution_num, self.plan_id, self.case_id, step_id, order, step_type, op_object, object_id, exec_operation,
                                        protocol, host, port, request_header, request_method, url_or_sql, input_params,
                                        response_to_check, check_rule, str(check_pattern), str(output_params), result[1], result[2], start_time, 0)
                            test_reporter.insert_report_for_case_step(data)
                    else:
                        test_case_step = TestCaseStep(self.execution_num, self.plan_id, self.case_id, step_id, order, step_type, op_object, object_id, exec_operation, request_header, \
                        request_method, url_or_sql, input_params, response_to_check, check_rule, \
                        check_pattern,  output_params, protocol, host, port, self.global_headers)
                        logger.info('======================开始运行测试步骤[第 %s 步, 步骤ID: %s]======================' % (order, step_id))
                        result = test_case_step.run(debug)

                    if not result[0]:
                        logger.error('步骤[第 %s 步, 步骤ID: %s]运行失败' % (order, step_id))
                        if not debug:
                            result = [result[0], result[1], '步骤[第 %s 步, 步骤ID: %s]运行失败' % (order, step_id)]
                        else:
                            result =  [result[0], result[1], '步骤[第 %s 步, 步骤ID: %s]运行失败:%s' % (order, step_id, result[2])]
                        break
            elif result[0] and not result[1]:
                logger.error('未查找到同测试用例关联的测试步骤')
                result = [False, '阻塞', '未找到与用例关联的测试步骤']
            else:
                logger.error('查找与测试用例[名称：%s, ID：%s]关联的用例步骤失败：%s' % (self.case_name, self.case_id, result[1]))
                result = [False, '阻塞',  '查找与测试用例[名称：%s, ID：%s]关联的用例步骤失败：%s' % (self.case_name, self.case_id, result[1])]
        except Exception as e:
            logger.error('%s' % e)
            result = [False, '阻塞', '%s' % e]
        finally:
            if not debug:
                logger.info('正在计算运行耗时')
                timestamp_for_end = time.time()
                time_took = int(timestamp_for_end - timestamp_for_start)
                days, hours, minutes, seconds = str(time_took//86400), str((time_took%86400)//3600), str(((time_took%86400)%3600)//60), str(((time_took%86400)%3600)%60)
                time_took = days + '天 '+ hours +'小时 '+ minutes + '分 ' +  seconds +'秒' # 运行耗时

                logger.info('正在记录用例运行结果到测试报告-用例执行明细表')
                data = (self.execution_num, self.plan_id, self.case_id, self.case_path, self.case_name, result[1], result[2], start_time, time_took)
                test_reporter.insert_report_for_case(data)
            return [result[0], result[1], result[2]]