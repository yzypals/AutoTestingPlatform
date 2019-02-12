#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time

from common.log import logger
from common.globalvar import test_platform_db
from common.globalvar import test_reporter
from test_case_step import TestCaseStep

class TestCase:
    def __init__(self, execution_num, plan_id, case_id, case_path, case_name, home_page):
        self.execution_num = execution_num
        self.plan_id = plan_id
        self.case_id = case_id
        self.case_path = case_path
        self.case_name = case_name
        self.home_page = home_page


    def run(self, debug):
        try:
            # 获取开始运行时间
            timestamp_for_start = time.time()
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            logger.info('正在查询测试用例[ID：%s, 名称：%s]关联的测试步骤' % (self.case_id, self.case_name))

            query = 'SELECT id, `order`, object_type, page_name, object, exec_operation, input_params, output_params,' \
                    'assert_type, assert_pattern, run_times, try_for_failure, object_id ' \
                    'FROM `website_ui_test_case_step` WHERE case_id=%s AND status=\'启用\' ORDER BY `order` ASC'
            data = (self.case_id,)
            result = test_platform_db.select_many_record(query, data)

            if result[0] and result[1]:
                records = result[1]
                result = [False, '阻塞', '没有找到与用例关联的测试步骤']
                for record in records:
                    step_id, order, object_type, page_name, op_object, exec_operation, input_params, \
                    output_params, assert_type, assert_pattern, run_times, try_for_failure, object_id = record

                    if object_type == '用例':
                        # 获取开始运行时间
                        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        level_list = op_object.split('->') # op_object即为case_path
                        case_name = level_list[len(level_list) - 1]
                        test_case = TestCase(self.execution_num, self.plan_id, object_id, op_object, case_name, self.home_page)
                        logger.info('======================开始运行测试步骤：第 %s 步======================' % order)
                        logger.info('所属用例：%s'% case_name)
                        logger.info('所属用例ID：%s'% self.case_id)
                        logger.info('步骤ID：%s' % step_id)
                        logger.info('步骤类型：执行用例')
                        logger.info('用例路径：%s' % op_object)
                        logger.info('用例ID：%s\n' % object_id)
                        result = test_case.run(debug)

                        if not debug:
                            logger.info('======================正在记录用例步骤运行结果到测试报告-用例步骤执行明细表======================')
                            data = (self.execution_num, self.plan_id, self.case_id, step_id, order, page_name, op_object, exec_operation, input_params, output_params,
                                                            assert_type, assert_pattern, run_times, try_for_failure, result[1], result[2], start_time, 0)
                            test_reporter.insert_report_for_case_step(data)
                    else:
                        test_case_step = TestCaseStep(self.execution_num, self.plan_id, self.case_id, step_id, order, object_type, page_name, op_object, exec_operation, input_params, \
                                                      output_params, assert_type, assert_pattern, run_times, try_for_failure,  object_id, self.home_page)
                        logger.info('======================开始运行测试步骤：第 %s 步======================' % order)
                        logger.info('所属用例：%s'% self.case_name)
                        logger.info('所属用例ID：%s'% self.case_id)
                        logger.info('步骤ID：%s' % step_id)
                        logger.info('步骤类型：操作%s' % object_type)
                        logger.info('操作对象：%s' % op_object)
                        logger.info('所在页面：%s' % page_name)
                        logger.info('执行操作：%s' % exec_operation)
                        logger.info('输入参数：%s' % input_params)
                        logger.info('断言类型：%s' % assert_type)
                        logger.info('断言模式：%s\n' % assert_pattern)

                        result = test_case_step.run(debug)

                    if not result[0]:
                        logger.error('------------------------------步骤运行失败--------------------------------------')
                        logger.info('所属用例名称：%s'% self.case_name)
                        logger.info('所属用例ID：%s'% self.case_id)
                        logger.info('步骤ID：%s' % step_id)
                        logger.info('步骤序号：第 %s 步' % order)
                        logger.info('步骤类型：操作%s' % op_object)
                        logger.info('所在页面：%s' % page_name)
                        logger.info('执行操作：%s' % exec_operation)
                        logger.info('输入参数：%s' % input_params)
                        logger.info('断言类型：%s' % assert_type)
                        logger.info('断言模式：%s' % assert_pattern)
                        logger.info('失败原因：%s' % result[2])
                        logger.info('--------------------------------------------------------------------')
                        logger.info('\n\n\n\n')


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
                result = [False, '阻塞',  '查找与用例关联的用测试步骤失败']
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



