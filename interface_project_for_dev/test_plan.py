#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time

from common.log import logger
from common.globalvar import test_platform_db
from common.globalvar import test_reporter
from test_case import TestCase

class TestPlan:
    def __init__(self, plan_id, plan_name, project_id, project_name, protocol, host, port, global_headers):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.project_id = project_id
        self.project_name = project_name
        self.protocol = protocol
        self.host = host
        self.port = port
        self.global_headers = global_headers


    def run(self, debug):
        try:
            # 获取开始运行时间
            timestamp_for_start = time.time()
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            logger.info('正在查询测试计划关联的测试用例')
            query = 'SELECT node_id, node_path, node_name FROM `website_api_case_tree_test_plan` WHERE plan_id = %s AND sub_node_num = 0 ORDER BY `order` ASC'
            data = (self.plan_id, )
            result = test_platform_db.select_many_record(query, data)
            if result[0] and result[1]:
                records = result[1]
                execution_num = str(int(time.time())) # 执行编号

                if not debug:
                    data = (execution_num, self.project_id, self.plan_id, self.project_name, self.plan_name, start_time, '', '', 0, 0, 0, 0, '')
                    logger.info('正在往测试报告-测试概况插入计划执行概要记录')
                    test_reporter.insert_report_for_summary(data)

                flag = False
                remark = ''
                for record in records:
                    plan_id = self.plan_id
                    case_id, case_path, case_name = record
                    test_case = TestCase(execution_num, plan_id, case_id, case_path, case_name, self.protocol, self.host, self.port, self.global_headers)
                    logger.info('======================开始运行测试用例[名称：%s, ID:%s]======================' % (case_name, case_id))
                    result = test_case.run(debug)
                    if not result[0]:
                        flag = True # 有运行出错的用例
                        remark = '存在运行失败、被阻塞的用例'

                if not debug:
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) # 结束运行时间
                    # 记录运行截止时间
                    timestamp_for_end = time.time()
                    logger.info('测试用例执行完毕，正在更新测试报告-测试概况表')
                    time_took = int(timestamp_for_end - timestamp_for_start)
                    days, hours, minutes, seconds = str(time_took//86400), str((time_took%86400)//3600), str(((time_took%86400)%3600)//60), str(((time_took%86400)%3600)%60)
                    time_took = days + '天 '+ hours +'小时 '+ minutes + '分 ' +  seconds +'秒' # 运行耗时

                    case_pass_num = test_reporter.get_case_num_by_run_result(execution_num, self.plan_id, '成功')   # 运行成功用例数
                    case_fail_num = test_reporter.get_case_num_by_run_result(execution_num, self.plan_id,  '失败')   # 运行失败用例数
                    case_block_num = test_reporter.get_case_num_by_run_result(execution_num,self.plan_id,  '阻塞')  # 运行被阻塞用例数
                    case_total_num = case_block_num + case_fail_num + case_pass_num

                    data = (end_time, time_took, case_total_num, case_pass_num, case_fail_num, case_block_num, remark, execution_num, self.plan_id)
                    test_reporter.update_report_for_summary(data)

                if flag:
                    return [False, '存在运行失败、被阻塞的用例']
                else:
                    return [True, '执行成功']
            elif result[0] and not result[1]:
                reason = '未查找到同测试计划关联的用例'
                logger.warn(reason)
                return [False, reason]
            else:
                reason = '查找同测试计划[名称：%s, ID：%s]关联的用例失败：%s' % (self.plan_name, self.plan_id, result[1])
                logger.error(reason)
                return [False, reason]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]